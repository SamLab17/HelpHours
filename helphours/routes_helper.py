from helphours import notifier, db, queue_handler, app, log
from flask import render_template, g, url_for
from helphours.models.visit import Visit
from datetime import datetime


def handle_line_form(request, curr_open_state):
    """
        Handle post requests in the view line page.
        Will return a boolean indicating whether the line should be
        open (True) or closed (False).
    """
    # Handle removing student, the line's "open state" should be unchanged.
    if 'finished' in request.form or 'removed' in request.form:
        handle_remove(request)
        return curr_open_state
    # Close the queue to new entries
    elif 'close' in request.form:
        return False
    # Open the queue to new entries
    elif 'open' in request.form:
        return True


def handle_remove(request):
    """
        Handles removing a student from the view queue
        page. This can be done either using the "Finish"
        button once a student is helped or the "Remove" button
        if a student is removed from the queue without being
        helped. Will notify new runner-up in the queue.
    """
    if 'finished' in request.form:
        uid = request.form['finished']
    elif 'removed' in request.form:
        uid = request.form['removed']
    # Remove the student from the queue and update the database
    remove_helper(uid, was_helped=('finished' in request.form.keys()), instructor_id=g.user.id)

    # Notify runner-up in the queue
    s = queue_handler.peek_runner_up()
    if s is not None and not s.notified:
        try:
            notifier.send_message(s.email, "Notification from {{COURSE_NAME}} Help Hours Queue",
                                  render_template("up_next_email.html", student_name=s.name, remove_code=s.eid,
                                                  view_link=app.config['WEBSITE_LINK'] + url_for('view')), 'html')
            s.notified = True
        except Exception as e:
            print(f"Failed to send email to {s.email}. {e}")


def get_place_str(place):
    """
        Formats a place in the queue with the appropriate suffix.
        i.e. 1 => "1st", 2 -> "2nd", etc
        Used in the email when someone joins the queue
    """
    place_str = str(place)
    if len(place_str) == 2 and place_str[0] == '1':
        return f"{place}th"
    elif place_str[-1] == '1':
        return f"{place}st"
    elif place_str[-1] == '2':
        return f"{place}nd"
    elif place_str[-1] == '3':
        return f"{place}rd"
    else:
        return f"{place}th"


def remove_helper(uid, was_helped=False, instructor_id=None):
    """
        Removes the student from the queue and updates the
        visit entry with the time they were removed.
    """
    queue_handler.remove(uid)
    v = Visit.query.filter_by(id=uid).first()
    if v is not None:
        v.time_left = datetime.utcnow()
        if was_helped:
            v.was_helped = 1
            v.instructor_id = instructor_id
        else:
            v.was_helped = 0
        db.session.commit()
    else:
        log.error(f"Did not find entry for {uid} in the visits table.")
