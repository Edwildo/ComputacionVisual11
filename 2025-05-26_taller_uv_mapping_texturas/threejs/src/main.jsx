import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import UVWorkflowDemo from './UVWorkflowDemo.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <UVWorkflowDemo />
  </StrictMode>,
)
