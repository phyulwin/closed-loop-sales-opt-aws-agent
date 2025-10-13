import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Replace 'phyulwin' and 'closed-loop-sales-opt-aws-agent' with your GitHub username and repo
export default defineConfig({
    base: '/closed-loop-sales-opt-aws-agent/',
    plugins: [react()],
})
