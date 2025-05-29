// src/components/DragControls.jsx
import { useThree, useFrame } from '@react-three/fiber'
import { useRef, useEffect } from 'react'

export default function DragControls() {
  const { camera, gl } = useThree()
  const isDragging = useRef(false)
  const prevPos = useRef([0, 0])

  useEffect(() => {
    const onDown = e => {
      isDragging.current = true
      prevPos.current = [e.clientX, e.clientY]
      gl.domElement.style.cursor = 'grabbing'
    }
    const onUp = () => {
      isDragging.current = false
      gl.domElement.style.cursor = 'grab'
    }
    const onMove = e => {
      if (!isDragging.current) return
      const [px, py] = prevPos.current
      const dx = (e.clientX - px) * 0.005
      const dy = (e.clientY - py) * 0.005
      camera.rotation.y -= dx
      camera.rotation.x -= dy
      prevPos.current = [e.clientX, e.clientY]
    }

    gl.domElement.addEventListener('pointerdown', onDown)
    window.addEventListener('pointerup', onUp)
    window.addEventListener('pointermove', onMove)
    gl.domElement.style.cursor = 'grab'

    return () => {
      gl.domElement.removeEventListener('pointerdown', onDown)
      window.removeEventListener('pointerup', onUp)
      window.removeEventListener('pointermove', onMove)
    }
  }, [camera, gl.domElement])

  // Fuerza actualización cada frame
  useFrame(() => {})

  return null
}
