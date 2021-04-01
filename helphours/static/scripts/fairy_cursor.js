/*
 * Code originally by Tim Holman: 
 * https://github.com/tholman/cursor-effects/blob/master/src/fairyDustCursor.js 
 * 
 * Converted to use classes by Samuel Laberge 2021
 * 
 */


class FairyDustCursor {

    constructor(options) {
        this.possibleColors = (options && options.colors) || [
            "#D61C59",
            "#E7D84B",
            "#1B8798",
        ]
        this.hasWrapperEl = options && options.elment
        this.element = this.hasWrapperEl || document.body
        this.width = window.innerWidth
        this.height = window.innerHeight
        this.cursor = { x: this.width / 2, y: this.width / 2 }
        this.lastPos = { x: this.width / 2, y: this.width / 2 }
        this.particles = []
        this.canvImages = []
        this.canvas
        this.context
        this.requestId
        this.char = "*"
        this.canvas = document.createElement("canvas")
        this.context = this.canvas.getContext("2d")
        this.canvas.style.top = "0px"
        this.canvas.style.left = "0px"
        this.canvas.style.pointerEvents = "none"
        this.mouseMoveFunc = this.onMouseMove.bind(this)
        this.touchMoveFunc = this.onTouchMove.bind(this)
        this.windowResizeFunc = this.onWindowResize.bind(this)

        if (this.hasWrapperEl) {
            this.canvas.style.position = "absolute"
            this.element.appendChild(canvas)
            this.canvas.width = element.clientWidth
            this.canvas.height = element.clientHeight
        } else {
            this.canvas.style.position = "fixed"
            this.element.appendChild(this.canvas)
            this.canvas.width = this.width
            this.canvas.height = this.height
        }

        this.context.font = "21px serif"
        this.context.textBaseline = "middle"
        this.context.textAlign = "center"

        this.possibleColors.forEach((color) => {
            let measurements = this.context.measureText(this.char)
            let bgCanvas = document.createElement("canvas")
            let bgContext = bgCanvas.getContext("2d")

            bgCanvas.width = measurements.width
            bgCanvas.height =
                measurements.actualBoundingBoxAscent +
                measurements.actualBoundingBoxDescent

            bgContext.fillStyle = color
            bgContext.textAlign = "center"
            bgContext.font = "21px serif"
            bgContext.textBaseline = "middle"
            bgContext.fillText(
                this.char,
                bgCanvas.width / 2,
                measurements.actualBoundingBoxAscent
            )

            this.canvImages.push(bgCanvas)
        })
        this.resumeEffect()
    }

    bindEvents() {
        this.element.addEventListener("mousemove", this.mouseMoveFunc)
        this.element.addEventListener("touchmove", this.touchMoveFunc)
        this.element.addEventListener("touchstart", this.touchMoveFunc)
        window.addEventListener("resize", this.windowResizeFunc)
    }

    unbindEvents() {
        this.element.removeEventListener("mousemove", this.mouseMoveFunc)
        this.element.removeEventListener("touchmove", this.touchMoveFunc)
        this.element.removeEventListener("touchstart", this.touchMoveFunc)
        window.removeEventListener("resize", this.windowResizeFunc)

    }

    pauseEffect() {
        this.unbindEvents()
        window.cancelAnimationFrame(this.requestId)
        this.clearParticles()
    }

    resumeEffect() {
        this.bindEvents()
        this.loop()
    }

    onWindowResize(e) {
        this.width = window.innerWidth
        this.height = window.innerHeight

        if (hasWrapperEl) {
            this.canvas.width = element.clientWidth
            this.canvas.height = element.clientHeight
        } else {
            this.canvas.width = width
            this.canvas.height = height
        }
    }

    onTouchMove(e) {
        if (e.touches.length > 0) {
            for (let i = 0; i < e.touches.length; i++) {
                addParticle(
                    e.touches[i].clientX,
                    e.touches[i].clientY,
                    this.canvImages[Math.floor(Math.random() * this.canvImages.length)]
                )
            }
        }
    }

    onMouseMove(e) {
        window.requestAnimationFrame(() => {
            if (this.hasWrapperEl) {
                const boundingRect = element.getBoundingClientRect()
                this.cursor.x = e.clientX - this.boundingRect.left
                this.cursor.y = e.clientY - this.boundingRect.top
            } else {
                this.cursor.x = e.clientX
                this.cursor.y = e.clientY
            }

            const distBetweenPoints = Math.hypot(
                this.cursor.x - this.lastPos.x,
                this.cursor.y - this.lastPos.y
            )

            if (distBetweenPoints > 1.5) {
                this.addParticle(
                    this.cursor.x,
                    this.cursor.y,
                    this.canvImages[Math.floor(Math.random() * this.possibleColors.length)]
                )

                this.lastPos.x = this.cursor.x
                this.lastPos.y = this.cursor.y
            }
        })
    }

    addParticle(x, y, color) {
        this.particles.push(new Particle(x, y, color))
    }

    updateParticles() {
        this.context.clearRect(0, 0, this.width, this.height)

        // Update
        for (let i = 0; i < this.particles.length; i++) {
            this.particles[i].update(this.context)
        }

        // Remove dead particles
        for (let i = this.particles.length - 1; i >= 0; i--) {
            if (this.particles[i].lifeSpan < 0) {
                this.particles.splice(i, 1)
            }
        }
    }

    loop() {
        this.updateParticles()
        this.requestId = requestAnimationFrame(this.loop.bind(this))
    }

    clearParticles() {
        this.context.clearRect(0, 0, this.width, this.height)
        this.canvImages.forEach(c => {})
        this.particles = []
    }

}

function Particle(x, y, canvasItem) {
    const lifeSpan = Math.floor(Math.random() * 30 + 60)
    this.initialLifeSpan = lifeSpan //
    this.lifeSpan = lifeSpan //ms
    this.velocity = {
        x: (Math.random() < 0.5 ? -1 : 1) * (Math.random() / 2),
        y: Math.random() * 0.7 + 0.9,
    }
    this.position = { x: x, y: y }
    this.canv = canvasItem

    this.update = function (context) {
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y
        this.lifeSpan--

        this.velocity.y += 0.02

        const scale = Math.max(this.lifeSpan / this.initialLifeSpan, 0)

        context.drawImage(
            this.canv,
            this.position.x - (this.canv.width / 2) * scale,
            this.position.y - this.canv.height / 2,
            this.canv.width * scale,
            this.canv.height * scale
        )
    }
}
