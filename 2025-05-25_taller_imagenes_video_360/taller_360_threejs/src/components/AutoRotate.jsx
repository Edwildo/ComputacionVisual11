// src/components/AutoRotate.jsx
import { useFrame, useThree } from '@react-three/fiber'

export default function AutoRotate({ speed = 0.1 }) {
  const { camera } = useThree()
  useFrame((_, delta) => {
    camera.rotation.y += speed * delta
  })
  return null
}
