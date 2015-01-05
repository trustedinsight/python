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

        var hOffset = h - 10;
        var wOffset = w - 10;

        var osc1 = new osc(0, 400, 0.09);
        var count = 1000; // 40
        var step = 1; //Math.ceil(w / count);
        var buffer = new ArrayBuffer(count * 4);
        var points = new Float32Array(buffer);

        function fill() {
            for (var i = 0; i < count; i++) {
                points[i] = osc1.getAmp();
            }
        }

        ctx.lineWidth = 1;
        ctx.strokeStyle = '#ffffff';
        ctx.fillStyle = 'rgb(50, 50, 80)';

        $("#minPulseLength").on('keydown', function (e) {

            if (e.keyCode == 13) {
                var v = $("#minPulseLength").val();
                osc1.min = v;
                console.log("minP: " + v);
            }

        });

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

            var gradients = 5;
            for (var z = -1; z < gradients; z++) {

                ctx.beginPath();
                ctx.moveTo(10, hOffset - (hOffset / 2 * ((z+1) / gradients)) );
                ctx.lineTo(w, hOffset - (hOffset / 2  * ((z+1) / gradients)) );
                ctx.strokeStyle = '#ff0000';
                ctx.stroke();

            }

            requestAnimationFrame(loop);
        }

        loop();

        /// oscillator object
        function osc(minn, maxx, spd) {

            var me = this,
                a = 0,
                max = getMax(),
                min = getMin(),
                speed = 0;

            setMax(maxx);
            setMin(minn);
            setSpeed(spd);

            this.getAmp = function () {

                a += this.speed;

                if (a >= 2.0) {
                    a = 0;
                }

                //return max * Math.sin(a * Math.PI);
                var waveVal = a < 1 ? this.min : this.max;
                // console.log(waveVal);
                return  waveVal;
            }

            function getMax() {
                return me.max;
            }

            function getMin() {
                return me.min;
            }

            function setMax(x) {
                me.max = hOffset - x;
            }

            function setMin(x) {
                me.min = hOffset - x;
            }

            function setSpeed(x) {
                me.speed = x;
            }

            return this;
        }

    }
)