import React, { useState } from 'react'
import { OrbitControls } from '@react-three/drei'
import { Physics } from '@react-three/cannon'
import Ground from './Ground'
import BoxObject from './BoxObject'
import Particles from './Particles'

export default function Scene() {
  const [explosions, setExplosions] = useState([])

  const handleCollision = (contact) => {
    const point = contact.bi.position
    setExplosions((prev) => [...prev, { id: Math.random(), position: [...point] }])
    setTimeout(() => {
      setExplosions((prev) => prev.slice(1))
    }, 1000)
  }

  return (
    <>
      <OrbitControls />
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 10, 5]} castShadow intensity={1} />
      <Physics gravity={[0, -9.81, 0]}>
        <Ground />
        <BoxObject onCollide={handleCollision} />
      </Physics>
      {explosions.map(e => (
        <Particles key={e.id} position={e.position} />
      ))}
    </>
  )
}
