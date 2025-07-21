import React, { useRef } from 'react'

export default function Particles({ position }) {
  const group = useRef()
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    position: [
      position[0] + (Math.random() - 0.5) * 0.5,
      position[1] + (Math.random() - 0.5) * 0.5,
      position[2] + (Math.random() - 0.5) * 0.5,
    ],
  }))

  return (
    <group ref={group}>
      {particles.map(p => (
        <mesh key={p.id} position={p.position}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshStandardMaterial color="hotpink" emissive="hotpink" />
        </mesh>
      ))}
    </group>
  )
}
