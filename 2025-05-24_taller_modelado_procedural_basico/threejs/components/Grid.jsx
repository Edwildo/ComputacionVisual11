import { useMemo } from 'react';

export default function Grid({ size, spacing }) {
  // Generamos posiciones elevadas en Y=0.5 para apoyar cubos en el "suelo"
  const positions = useMemo(() => {
    const pos = [];
    for (let x = 0; x < size; x++) {
      for (let z = 0; z < size; z++) {
        // [X, Y (half the height), Z]
        pos.push([x * spacing, 0.5, z * spacing]);
      }
    }
    return pos;
  }, [size, spacing]);

  return (
    <>
      {positions.map((p, i) => (
        <mesh key={i} position={p}>
          <boxGeometry args={[1, 1, 1]} />
          <meshStandardMaterial />
        </mesh>
      ))}
    </>
  );
}