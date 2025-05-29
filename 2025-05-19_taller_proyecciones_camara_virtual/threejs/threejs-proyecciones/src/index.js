import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

// Obtiene el elemento donde montamos
const container = document.getElementById('root');
// Crea el root
const root = createRoot(container);
// Renderiza la app
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
