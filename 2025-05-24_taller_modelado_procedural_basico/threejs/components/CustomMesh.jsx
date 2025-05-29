import { useRef, useEffect } from 'react';
import { BufferGeometry, Float32BufferAttribute } from 'three';

export default function CustomMesh({ position }) {
  const ref = useRef();

  useEffect(() => {
    const geom = new BufferGeometry();
    const verts = new Float32Array([
      0,0,0, 1,0,0, 1,1,0, 0,1,0,
      0,1,1, 1,1,1, 1,0,1, 0,0,1
    ]);
    const tris = [
      0,2,1, 0,3,2, 2,3,4, 2,4,5,
      1,2,5, 1,5,6, 0,7,4, 0,4,3,
      5,4,7, 5,7,6, 0,6,7, 0,1,6
    ];
    geom.setAttribute('position', new Float32BufferAttribute(verts, 3));
    geom.setIndex(tris);
    geom.computeVertexNormals();
    ref.current.geometry = geom;
  }, []);

  return (
    <mesh ref={ref} position={position}>
      <meshStandardMaterial />
    </mesh>
  );
}
