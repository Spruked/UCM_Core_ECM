# UCM Core ECM Frontend

A modern React + Vite TypeScript frontend for the UCM Core ECM philosophical reasoning system.

## Features

- **Query Input**: Text area for entering philosophical queries
- **File Upload**: Support for uploading `.txt`, `.md`, and `.json` files containing claims or texts
- **Result Display**: Structured rendering of tribunal verdicts, philosopher verdicts, and meta-analysis
- **Authentication**: API key handling via environment variables
- **Responsive UI**: Clean, modern interface built with React and TypeScript

## Quick Start

### Prerequisites
- Node.js 16+
- Running UCM Core ECM backend on `http://localhost:8000`

### Installation
```bash
cd frontend
npm install
```

### Configuration
```bash
cp .env.example .env
# Edit .env to set VITE_API_BASE and VITE_API_KEY
```

### Development
```bash
npm run dev  # Starts on http://localhost:5173
```

### Build
```bash
npm run build
npm run preview  # Preview production build
```

## Environment Variables

- `VITE_API_BASE`: Backend API URL (default: `http://localhost:8000`)
- `VITE_API_KEY`: API key for authentication (matches backend `ECM_API_KEY`)

## Components

### QueryForm
- Text input for queries
- File upload with automatic content loading
- Submit button with loading state
- Error handling and display

### ResultCard
- Verdict status and confidence bar
- Philosopher verdict breakdown
- Meta-analysis details (epistemic inevitability)

## API Integration

The frontend communicates with the FastAPI backend via Axios:

- `POST /api/adjudicate`: Submit queries for tribunal deliberation
- Authentication via `Authorization: Bearer <API_KEY>` header

## Development

- Built with Vite for fast development
- TypeScript for type safety
- ESLint for code quality
- Hot reload during development

## License

MIT License - see root [LICENSE](../LICENSE) for details.
