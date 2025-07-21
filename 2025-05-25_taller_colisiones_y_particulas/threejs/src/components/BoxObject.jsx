import React from 'react'
import { useBox } from '@react-three/cannon'

export default function BoxObject({ onCollide }) {
  const [ref] = useBox(() => ({
    mass: 1,
    position: [0, 5, 0],
    onCollide: (e) => onCollide(e.contact),
  }))

  return (
    <mesh ref={ref} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}
