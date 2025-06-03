import { Canvas } from '@react-three/fiber'
import ShaderSphere from './ShaderSphere.jsx'

function App() {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <ShaderSphere />
    </Canvas>
  )
}

export default App