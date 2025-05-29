import { useMemo } from 'react';

export default function Spiral({ turns, pointsPerTurn, radius }) {
  const positions = useMemo(() => {
    const pos = [];
    const total = turns * pointsPerTurn;
    for (let i = 0; i < total; i++) {
      const t = i / pointsPerTurn;
      const angle = t * Math.PI * 2;
      const r = (radius * t) / turns;
      pos.push([Math.cos(angle) * r, 0, Math.sin(angle) * r]);
    }
    return pos;
  }, [turns, pointsPerTurn, radius]);

  return (
    <>
      {positions.map((p, i) => (
        <mesh key={i} position={p}>
          <cylinderGeometry args={[0.25,0.25,1,16]} />
          <meshStandardMaterial />
        </mesh>
      ))}
    </>
  );
}
