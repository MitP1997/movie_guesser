! function() {
  "use strict";
  // ==== init ====
  var screen = ge1doot.screen.init("screen", null, true),
    ctx = screen.ctx,
    pointer = screen.pointer.init({
      move: fire,
      down: fire
    }),
    canvas = document.getElementById("canvas"),
    ctx = canvas.getContext("2d"),
    scale = 4,
    sw = canvas.width = screen.width / scale,
    sh = canvas.height = screen.height / scale,
    ram = new Uint16Array(sw * sh),
    fires = [],
    maxFires = 800,
    nFire = 0;
  // ==== write text ====
  ctx.font = "bold 40px arial";
  ctx.fillStyle = "rgba(255,0,0,1)";
  ctx.fillText("JAM", 5, 80);
  var img = ctx.getImageData(0, 0, sw, sh);
  var bytes = img.data;
  for (var i = 0; i < sh; i += 2) {
    for (var j = 0; j <= sw; j += 2) {
      if (bytes[(i * sw + j) * 4 + 3] != 0) fires[nFire++] = [i * 1, j * 1]
    }
  }
  nFire = 0;
  var bytes = img.data;
  // ==== add more fire ====
  function fire() {
      fires[nFire++] = [pointer.pos.y / 4, pointer.pos.x / 4];
      if (nFire > maxFires) nFire = 0;
    }
    // ==== main loop ====
  function run() {
      requestAnimationFrame(run);
      // ==== maintain fire ====
      for (var i = 0; i < maxFires; i++) {
        if (fires[i]) {
          var k = ((0.5 + fires[i][0] | 0) * sw + (0.5 + fires[i][1] | 0));
          ram[k] = 1024;
        }
      }
      // ==== render fire ====
      for (var i = 0; i < sh; i++) {
        for (var j = 0; j <= sw; j++) {
          var p = i * sw + j;
          var ap = p + sw - (0.5 + Math.random() | 0);
          var nc = ((ram[ap] || 0) + (ram[ap + 1] || 0) + (ram[ap + sw] || 0) + (ram[ap - sw + 1] || 0)) * 0.24;
          ram[p] = nc;
          var k = p * 4;
          bytes[k] = nc;
          bytes[k + 1] = nc / 3;
          bytes[k + 3] = 255;
        }
      }
      ctx.putImageData(img, 0, 0);
    }
    // ==== start animation ====
  requestAnimationFrame(run);
}();