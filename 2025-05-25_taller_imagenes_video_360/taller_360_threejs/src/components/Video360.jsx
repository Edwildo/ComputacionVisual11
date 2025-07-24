// src/components/Video360.jsx
import React, { useRef, useEffect } from 'react'
import * as THREE from 'three'

export default function Video360() {
  const meshRef = useRef()           // ← Declaramos la ref aquí

  useEffect(() => {
    const video = document.createElement('video')
    video.src = '/video360.mp4'
    video.crossOrigin = 'anonymous'
    video.loop = true
    video.muted = true
    video.playsInline = true
    video.play().catch(() => {
      console.warn('Autoplay falló, esperando interacción del usuario')
    })

    const texture = new THREE.VideoTexture(video)
    texture.minFilter = THREE.LinearFilter
    texture.magFilter = THREE.LinearFilter
    texture.generateMipmaps = false

    // Espera a que meshRef.current exista
    if (meshRef.current) {
      meshRef.current.material.map = texture
      meshRef.current.material.needsUpdate = true
    }
  }, [])

  return (
    <mesh ref={meshRef} scale={[-10, 10, 10]}>
      <sphereGeometry args={[10, 32, 16]} />
      <meshBasicMaterial side={THREE.BackSide} />
    </mesh>
  )
}
