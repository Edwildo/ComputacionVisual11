export const dynamicVertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

export const dynamicFragmentShader = `
  uniform float uTime;
  uniform vec2 uMouse;
  varying vec2 vUv;

  void main() {
    float dist = distance(vUv, uMouse);
    vec3 color = vec3(sin(uTime + dist * 10.0), cos(uTime), sin(dist * 10.0));
    gl_FragColor = vec4(color, 1.0);
  }
`;
