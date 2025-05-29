// App.jsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import Grid from './components/Grid'
import Spiral from './components/Spiral'
import CustomMesh from './components/CustomMesh'

export default function App() {
  return (
    <Canvas
      camera={{ position: [10, 10, 15], fov: 60 }}
      style={{ height: '100vh', width: '100vw' }}
    >
      <ambientLight intensity={0.3} />
      <directionalLight position={[5, 10, 5]} intensity={1} />
      <Grid size={5} spacing={2} />
      <Spiral turns={3} pointsPerTurn={20} radius={5} />
      <CustomMesh position={[8, 0, 0]} />
      <OrbitControls />
    </Canvas>
  )
}
