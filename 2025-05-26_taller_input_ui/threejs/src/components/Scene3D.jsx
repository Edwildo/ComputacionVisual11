import React, { useRef, useState, useCallback } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import * as THREE from 'three';
import PropTypes from 'prop-types';

const LABEL_STYLE = {
    background: 'rgba(0,0,0,0.7)',
    color: 'white',
    padding: '4px 8px',
    borderRadius: '4px',
    fontSize: '14px',
    pointerEvents: 'none',
};

export default function Scene3D({ rotationSpeed = 0.01 }) {
    const meshRef = useRef();
    const { mouse, size } = useThree();
    const [isActive, setIsActive] = useState(false);
    const [position, setPosition] = useState([0, 0, 0]);

    // Handle keyboard controls
    const handleKeyDown = useCallback(
        (e) => {
            setPosition((prev) => {
                let [x, y, z] = prev;
                switch (e.key) {
                    case 'ArrowUp':
                        return [x, y + 0.1, z];
                    case 'ArrowDown':
                        return [x, y - 0.1, z];
                    case 'ArrowLeft':
                        return [x - 0.1, y, z];
                    case 'ArrowRight':
                        return [x + 0.1, y, z];
                    case 'r':
                    case 'R':
                        return [0, 0, 0];
                    default:
                        return prev;
                }
            });
        },
        []
    );

    React.useEffect(() => {
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [handleKeyDown]);

    // Animate rotation and follow mouse if active
    useFrame(() => {
        if (!meshRef.current) return;
        meshRef.current.rotation.x += rotationSpeed;
        meshRef.current.rotation.y += rotationSpeed;

        if (isActive) {
            // Map mouse [-1,1] to scene coordinates (e.g., [-2,2])
            const x = THREE.MathUtils.lerp(-2, 2, (mouse.x + 1) / 2);
            const y = THREE.MathUtils.lerp(-2, 2, (mouse.y + 1) / 2);
            meshRef.current.position.x = x;
            meshRef.current.position.y = y;
            meshRef.current.position.z = position[2];
        } else {
            meshRef.current.position.set(...position);
        }
    });

    return (
        <group>
            <mesh
                ref={meshRef}
                onClick={() => setIsActive((a) => !a)}
                castShadow
                receiveShadow
            >
                <boxGeometry args={[1, 1, 1]} />
                <meshStandardMaterial color={isActive ? 'orange' : 'hotpink'} />
                <Html center distanceFactor={1.5}>
                    <div style={LABEL_STYLE}>
                        {isActive ? 'Activo' : 'Inactivo'}
                    </div>
                </Html>
            </mesh>
        </group>
    );
}

Scene3D.propTypes = {
    rotationSpeed: PropTypes.number,
};