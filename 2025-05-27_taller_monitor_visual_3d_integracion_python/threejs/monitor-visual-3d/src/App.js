import React, { useEffect, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { Box } from '@react-three/drei';
import socket from './utils/socket';

function App() {
  const [detections, setDetections] = useState(0);

  useEffect(() => {
    socket.on('data', ({ detections }) => {
      setDetections(detections);
    });
    return () => socket.off('data');
  }, []);

  return (
    <Canvas>
      <ambientLight />
      <spotLight position={[10, 10, 10]} />
      <Box scale={[detections, detections, detections]}>
        <meshStandardMaterial
          color={`rgb(${Math.min(detections*50,255)}, 0, 0)`}
        />
      </Box>
    </Canvas>
  );
}

export default App;
