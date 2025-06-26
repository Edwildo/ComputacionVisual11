# Taller - Introducción a Realidad Aumentada Web: Marcadores con AR.js

## Objetivo

El objetivo de este taller es implementar una experiencia básica de realidad aumentada en el navegador, utilizando AR.js y Three.js. Los participantes aprenderán a proyectar un modelo 3D sobre un marcador físico y activar interacciones o animaciones al detectar el marcador.

## Flujo de Trabajo

### 1. Preparar la Estructura HTML:
El código base incluye los scripts de AR.js y A-Frame, que permiten integrar la realidad aumentada en el navegador:

```html
<html>
  <head>
    <script src="https://aframe.io/releases/1.3.0/aframe.min.js"></script>
    <script src="https://cdn.rawgit.com/jeromeetienne/ar.js/2.3.1/aframe/build/aframe-ar.js"></script>
  </head>
  <body style="margin: 0; overflow: hidden;">
    <a-scene embedded arjs>
      <a-marker preset="hiro">
        <a-box position="0 0.5 0" material="color: red;"></a-box>
      </a-marker>
      <a-entity camera></a-entity>
    </a-scene>
  </body>
</html>
