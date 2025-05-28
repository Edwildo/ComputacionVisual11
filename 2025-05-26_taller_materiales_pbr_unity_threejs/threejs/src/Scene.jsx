import { Canvas, useLoader } from '@react-three/fiber'
import { OrbitControls, useTexture } from '@react-three/drei'
import { Leva, useControls } from 'leva'

function Scene() {
    const [colorMap, normalMap, roughnessMap] = useTexture([
        '/textures/Bricks097_1K-JPG_Color.jpg',    // map
        '/textures/Bricks097_1K-JPG_NormalGL.jpg', // normalMap
        '/textures/Bricks097_1K-JPG_Roughness.jpg' // roughnessMap
    ]);

    // Controles de Leva
    const { roughness, metalness } = useControls({
        roughness: { value: 0.5, min: 0, max: 1 },
        metalness: { value: 0.5, min: 0, max: 1 }
    })

    return (
        <>
            <ambientLight intensity={0.3} />
            <directionalLight position={[5, 5, 5]} intensity={1} />

            {/* Cubo con material PBR */}
            <mesh position={[0, 0.5, 0]}>
                <boxGeometry args={[1, 1, 1]} />
                {/* Material con texturas */}
                <meshStandardMaterial
                    map={colorMap}
                    normalMap={normalMap}
                    roughnessMap={roughnessMap}
                    metalness={0.0} // Ladrillos no son metálicos
                />
            </mesh>

            {/* Esfera con material básico */}
            <mesh position={[2, 1, 0]}>
                <sphereGeometry args={[0.7, 32, 32]} />
                <meshBasicMaterial color="hotpink" />
            </mesh>

            {/* Piso */}
            <mesh rotation={[-Math.PI / 2, 0, 0]}>
                <planeGeometry args={[10, 10]} />
                <meshStandardMaterial color="#ddd" />
            </mesh>
        </>
    )
}

export default function App() {
    return (
        <>
            <Leva />
            <div style={{ width: '100vw', height: '100vh', position: 'fixed', top: 0, left: 0 }}>
                <Canvas>
                    <Scene style={{ width: '50vw', height: '50vh', position: 'fixed', top: 0, left: 0 }}/>
                    <OrbitControls />
                    <axesHelper args={[5]} />
                </Canvas>
            </div>
        </>
    )
}