/**
 *    Wave oscillators by Ken Fyrstenberg Nilsen
 *    http://abdiassoftware.com/
 *
 *    CC-Attribute 3.0 License
 */


$(function () {


        var ctx = canvas.getContext('2d');
        var w, h;

        canvas.width = w = window.innerWidth * 0.9;
        canvas.height = h = window.innerHeight * 0.9;

        var osc1 = new osc(0, 400, 0.09);
        var horizon = h * 0.4; // the bigger this gets, the lower the wave offsets
        var count = 1000; // 40
        var step = 1; //Math.ceil(w / count);
        var buffer = new ArrayBuffer(count * 4);
        var points = new Float32Array(buffer);

        // Change wave amplitude
        //osc1.max = 450;
        //osc1.min = -450;

        // Change wait time
        //osc1.speed = 0.2

        function fill() {
            for (var i = 0; i < count; i++) {
                points[i] = osc1.getAmp();
            }
        }

        ctx.lineWidth = 1;
        ctx.strokeStyle = '#ffffff';
        ctx.fillStyle = 'rgb(50, 50, 80)';

        function loop() {

            var i;

            /// move points to the left
            for (i = 0; i < count - 1; i++) {
                points[i] = points[i + 1];
            }

            /// get a new point
            points[count - 1] = osc1.getAmp(); //, osc2, osc3);

            //ctx.clearRect(0, 0, w, h);
           ctx.fillRect(0, 0, w, h);

            /// render wave
            ctx.beginPath();
            ctx.moveTo(0, points[0]);

            for (i = 1; i < count; i++) {
                ctx.lineTo(i * step, points[i]);
            }

            ctx.strokeStyle = '#ffffff';
            ctx.stroke();

            // 0

            ctx.beginPath();
            ctx.moveTo(10, h - 10);
            ctx.lineTo(w, h - 10);
            ctx.strokeStyle = '#ff0000';
            ctx.stroke();

            requestAnimationFrame(loop);
        }

        loop();

/// oscillator object
        function osc(minn, maxx, spd) {

            this.max = maxx;
            this.min = minn;
            this.speed = spd;

            var me = this,
                a = 0,
                max = getMax(),
                min = getMin();

            this.getAmp = function () {

                a += this.speed;

                if (a >= 2.0) {
                    a = 0;
                }

                //return max * Math.sin(a * Math.PI);
                var waveVal = a < 1 ? this.min : this.max;
                console.log(waveVal);
                return  waveVal;
            }

            function getMax() {
                return me.max;
            }

            function getMin() {
                return me.min;
            }

            return this;
        }

    }
)