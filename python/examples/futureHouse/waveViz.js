/**
 *    Wave oscillators by Ken Fyrstenberg Nilsen
 *    http://abdiassoftware.com/
 *
 *    CC-Attribute 3.0 License
 */


  $(function() {

          var ctx = canvas.getContext('2d');
          var w, h;

          canvas.width = w = window.innerWidth * 0.9;
          canvas.height = h = window.innerHeight * 0.9;

          var osc1 = new osc(400, 100, 0.05);
          var horizon = h * 0.2; // the bigger this gets, the lower the wave offsets
          var count = 100; // 40
          var step = 10; //Math.ceil(w / count);
          var buffer = new ArrayBuffer(count * 4);
          var points = new Float32Array(buffer);

// Change wave amplitude
//osc1.max = 450;
//osc1.min = -450;

// Change wait time
//osc1.speed = 0.2

          function fill() {
              for (var i = 0; i < count; i++) {
                  points[i] = mixer(osc1);
              }
          }

          ctx.lineWidth = 5;
          ctx.strokeStyle = '#ffffff';
          ctx.fillStyle = 'rgb(50, 50, 80)';

          function loop() {

              var i;

              /// move points to the left
              for (i = 0; i < count - 1; i++) {
                  points[i] = points[i + 1];
              }

              /// get a new point
              points[count - 1] = mixer(osc1) //, osc2, osc3);

              //ctx.clearRect(0, 0, w, h);
              ctx.fillRect(0, 0, w, h);

              /// render wave
              ctx.beginPath();
              ctx.moveTo(0, points[0]);

              for (i = 1; i < count; i++) {
                  ctx.lineTo(i * step, points[i]);
              }

              ctx.stroke();

              requestAnimationFrame(loop);
          }

          loop();

/// oscillator object
          function osc(maxx, minn, spd) {

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
                  return a < 1 ? max : min;
              }

              function getMax() {
                  return me.max;
              }

              function getMin() {
                  return me.min;
              }

              return this;
          }

          function mixer(osc) {

              var d = arguments.length,
                  i = d,
                  sum = 0;

              if (d < 1) return 0;

              while (i--) sum += arguments[i].getAmp();

              console.log("1: " + osc.getAmp());
              console.log("2: " + sum);
              console.log("3: " + d + horizon);
              console.log("4: " + horizon);

              // return osc.getAmp() + horizon;
              return sum / d + horizon;
              //return arguments[i].getAmp() + horizon;


          }
      }
)