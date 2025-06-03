uniform float uTime;
varying vec2 vUv;
varying vec3 vPosition;

void main() {
  float gradient = vPosition.y * 0.5 + 0.5;
  float pulse = sin(uTime * 2.0 + vPosition.x * 2.0) * 0.5 + 0.5;
  float levels = 4.0;
  float toon = floor(gradient * levels) / levels;
  vec3 color = vec3(toon, pulse, 1.0 - toon);
  gl_FragColor = vec4(color, 1.0);
}