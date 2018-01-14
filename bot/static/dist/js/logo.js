window.requestAnimFrame = (function(){
  return  window.requestAnimationFrame       || 
          window.webkitRequestAnimationFrame || 
          window.mozRequestAnimationFrame    || 
          window.oRequestAnimationFrame      || 
          window.msRequestAnimationFrame     || 
          function( callback ){
            window.setTimeout(callback, 1000 / 60);
          };
})();

(function(){

  $(function(){ gears.setup(); });

  var global = {};
  
  var gears = {
    setup:function(){
      this.canvas = $('#gears')[0];
      this.canvas.width = 480;
      this.canvas.height = 480;
      this.cxt = this.canvas.getContext('2d');
      global.whiteGradient = this.cxt.createLinearGradient(0,0,0,this.canvas.height);
      global.whiteGradient.addColorStop("0","white");
      global.whiteGradient.addColorStop("1","rgba(255,255,255,.5)");
      global.toHue = Math.round(Math.random()*9)*20;
      global.hue = global.toHue;
      global.colorGradient = this.cxt.createLinearGradient(0,0,0,this.canvas.height);
      global.colorGradient.addColorStop("0","hsla("+global.hue+",100%,30%,1)");
      global.colorGradient.addColorStop("0.5","hsla("+global.hue+",100%,50%,1)");
      global.colorGradient.addColorStop("1","hsla("+global.hue+",100%,10%,1)");
      this.cxt.lineWidth = 16;
      this.gears = [gear(128,this.canvas), gear(96,this.canvas), gear(64,this.canvas), gear(32,this.canvas)];
      this.draw();
      window.setTimeout(function changeHue(){
        global.toHue = Math.round(Math.random()*9)*20;
        window.setTimeout(changeHue, Math.round(Math.random()*1000+10000));
      }, Math.round(Math.random()*1000+10000));
    },
    draw:function(){
      this.cxt.clearRect(0,0,this.canvas.width,this.canvas.height);
      this.cxt.lineWidth = 16;
      for(var i = 0, size = this.gears.length; i<size; ++i) {
        this.gears[i].draw(this.cxt, this.canvas);
      }
      this.adjust2Hue();
      window.requestAnimFrame(function(){ gears.draw(); });
    },
    adjust2Hue:function(){
      if (global.hue === global.toHue) return;
      if (Math.abs(global.hue - global.toHue) > Math.abs(global.hue - global.toHue + 360))
        global.toHue += 360
        
      if (Math.abs(global.hue-global.toHue) < 1.) {
        global.hue = global.toHue;
      } else {
        global.hue += (global.toHue-global.hue)/100;
        global.colorGradient = this.cxt.createLinearGradient(0,0,0,this.canvas.height);
        global.colorGradient.addColorStop("0","hsla("+global.hue+",100%,30%,1)");
        global.colorGradient.addColorStop("0.5","hsla("+global.hue+",100%,50%,.8)");
        global.colorGradient.addColorStop("1","hsla("+global.hue+",100%,50%,0)");
      }
    }
  };
  
  var gear = function(radius,canvas){
    return {
      init:function(){
        var cxt = canvas.getContext('2d');
        this.radius = radius;
        this.angle=Math.random() * Math.PI * 2;
        this.newSpeedValue = 0;
        this.newSpeed();
        this.speed = Math.round(Math.random())==1?-0.1:0.1;
        this.timerInit = 50;
        this.timer = this.timerInit;
        this.last = this.radius == 128;
        this.bars = [];
        this.numBars = 1;
        do {
          this.numBars++;
          if (this.numBars > 5)
            break;
        } while(Math.round(Math.random()) == 0 || this.numBars < 2);
        this.newBars = [];
        this.newBars.length = this.numBars;
        this.makeNewBars();
        for(var i = 0; i < this.numBars-1; i++){
          this.bars[i] = this.newBars[i];
        }
        this.hue = this.toHue;
        if (this.last) {
          this.newSpeedValue = .01;
          this.newBars = this.bars = [Math.PI];
        }
        return this;
      },
      draw:function(cxt, canvas){
        if (!this.last) {
          this.timer -=1;
          if (this.timer == 0) {
            this.timer = this.timerInit;
            this.newSpeed();
            this.makeNewBars();
          }
        }
        if (this.last) {
          this.gradient = global.whiteGradient;
          this.newSpeedValue = .01;
        } else {
          this.gradient = global.colorGradient;
        }
        this.adjust();
        this.angle+=this.speed;
        var sum = 0;
        cxt.save();
        for(var i = 0; i < this.numBars; i++) {
          cxt.beginPath();
          cxt.strokeStyle = this.gradient;
          cxt.arc(
            canvas.width/2,
            canvas.height/2,
            this.radius,
            this.angle - sum - this.bars[i]*.9,
            this.angle - sum - this.bars[i]*.1
          );
          cxt.stroke();
          sum += this.bars[i];
        }
        cxt.restore();
      },
      newSpeed:function(){
        var reverse = true;
        if (!this.last) {
          reverse = !!Math.round(Math.random());
        }
        this.newSpeedValue = (reverse?-1:1) * Math.random()/10 + .01;
      },
      adjust:function(){
        if (Math.abs(this.speed-this.newSpeedValue) < .001) {
          this.speed = this.newSpeedValue;
        } else {
          this.speed += (this.newSpeedValue-this.speed)/10;
        }
        for(var i = 0; i < this.numBars; i++) {
          if (Math.abs(this.bars[i]-this.newBars[i]) < .001) {
            this.bars[i] = this.newBars[i];
          } else {
            this.bars[i] += (this.newBars[i]-this.bars[i])/100;
          }
        }
      },
      makeNewBars:function(){
        var remaining = Math.PI*2;
        for(var i = 0; i < this.numBars-1; i++){
          var width = Math.random()*remaining;
          remaining -= width;
          this.newBars[i] = width;
        }
        this.newBars[this.numBars-1] = remaining;
      }
    }.init();
  }

})()