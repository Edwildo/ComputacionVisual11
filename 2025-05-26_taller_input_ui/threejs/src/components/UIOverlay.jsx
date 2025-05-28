import React, { useCallback } from 'react';
import { useControls } from 'leva';
import { Html } from '@react-three/drei';
import PropTypes from 'prop-types';

const colorOptions = {
    orange: '#FFA500',
    hotpink: '#FF69B4',
    lightblue: '#ADD8E6',
};

function UIOverlay({
    rotationSpeed,
    setRotationSpeed,
    color,
    setColor,
    onResetPosition,
    mouseTracking,
    setMouseTracking = () => {},
}) {
    // Leva controls
    useControls('Controls', {
        rotationSpeed: {
            value: rotationSpeed,
            min: 0,
            max: 0.1,
            step: 0.001,
            onChange: setRotationSpeed,
        },
        color: {
            options: Object.keys(colorOptions),
            value: Object.keys(colorOptions).find((key) => colorOptions[key] === color) || 'orange',
            onChange: (val) => {
                if (typeof setColor === 'function') {
                    setColor(colorOptions[val]);
                }
            },
        },
        'Reset Position': button(onResetPosition),
    });

    // Handler for mouse tracking toggle
    const handleMouseTrackingToggle = useCallback(() => {
        setMouseTracking((prev) => !prev);
    }, [setMouseTracking]);

    return (
        <Html position={[0, 0, 0]} style={{ pointerEvents: 'auto' }}>
            <div style={{ position: 'fixed', top: 20, right: 20, zIndex: 1000 }}>
                <button
                    onClick={handleMouseTrackingToggle}
                    style={{
                        padding: '8px 16px',
                        fontSize: '1rem',
                        borderRadius: '4px',
                        border: 'none',
                        background: mouseTracking ? '#4caf50' : '#f44336',
                        color: '#fff',
                        cursor: 'pointer',
                        marginTop: '8px',
                    }}
                >
                    {mouseTracking ? 'Desactivar seguimiento de mouse' : 'Activar seguimiento de mouse'}
                </button>
            </div>
        </Html>
    );
}

// Helper for Leva button
function button(fn) {
    return {
        value: undefined,
        onClick: fn,
    };
}

UIOverlay.propTypes = {
    rotationSpeed: PropTypes.number.isRequired,
    setRotationSpeed: PropTypes.func.isRequired,
    color: PropTypes.string.isRequired,
    setColor: PropTypes.func.isRequired,
    onResetPosition: PropTypes.func.isRequired,
    mouseTracking: PropTypes.bool.isRequired,
    setMouseTracking: PropTypes.func,
};

// Mueve el botón a la esquina inferior derecha y hazlo menos invasivo visualmente
UIOverlay.defaultProps = {
    setMouseTracking: () => {},
};

// Puedes ajustar el estilo del botón aquí si lo deseas
const buttonContainerStyle = {
    position: 'fixed',
    bottom: 24,
    right: 24,
    zIndex: 1000,
    background: 'rgba(255,255,255,0.85)',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    padding: '8px',
    display: 'flex',
    alignItems: 'center',
};

export default UIOverlay;