import React from 'react'
import { useBox } from '@react-three/cannon'

export default function Ground() {
  const [ref] = useBox(() => ({
    type: 'Static',
    position: [0, -0.5, 0],
    args: [10, 1, 10],
  }))

  return (
    <mesh ref={ref} receiveShadow>
      <boxGeometry args={[10, 1, 10]} />
      <meshStandardMaterial color="lightblue" />
    </mesh>
  )
}
    