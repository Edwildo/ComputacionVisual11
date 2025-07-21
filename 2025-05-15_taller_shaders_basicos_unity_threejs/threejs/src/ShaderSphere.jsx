import { useRef } from 'react'
import { useFrame, extend } from '@react-three/fiber'
import { shaderMaterial } from '@react-three/drei'
import vertexShader from './shaders/vertexShader.glsl'
import fragmentShader from './shaders/fragmentShader.glsl'

const MyShaderMaterial = shaderMaterial(
  { uTime: 0 },
  vertexShader,
  fragmentShader
)

extend({ MyShaderMaterial })

export default function ShaderSphere() {
  const ref = useRef()

  useFrame((state) => {
    ref.current.uTime = state.clock.getElapsedTime()
  })

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <myShaderMaterial ref={ref} />
    </mesh>
  )
}
