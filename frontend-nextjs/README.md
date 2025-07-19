# 🎬 Story-to-Video Generator - Next.js Frontend

A modern, responsive Next.js frontend for the AI-powered story-to-video generation workflow.

## ✨ Features

- **Modern UI/UX**: Beautiful, responsive design with smooth animations
- **5-Phase Workflow**: Clear step-by-step process with visual progress indicators
- **Real-time Progress**: Live updates during video generation
- **File Downloads**: Easy download of all generated assets
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Mobile Responsive**: Works perfectly on all device sizes

## 🏗️ Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion for smooth transitions
- **Icons**: Lucide React for consistent iconography
- **HTTP Client**: Axios for API communication
- **Notifications**: React Hot Toast for user feedback
- **TypeScript**: Full type safety throughout the application

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API server running (see main project README)

### Installation

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend-nextjs
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
frontend-nextjs/
├── app/
│   ├── globals.css          # Global styles and Tailwind imports
│   ├── layout.tsx           # Root layout with providers
│   └── page.tsx             # Main page with workflow logic
├── components/
│   ├── ui/                  # Reusable UI components
│   │   ├── Button.tsx       # Button component with variants
│   │   ├── Card.tsx         # Card component
│   │   └── Progress.tsx     # Progress bar component
│   ├── WorkflowSteps.tsx    # Workflow progress indicator
│   ├── Phase1PromptInput.tsx    # Phase 1: Story prompt input
│   ├── Phase2EnhancedStory.tsx  # Phase 2: Enhanced story review
│   ├── Phase3Confirmation.tsx   # Phase 3: Generation confirmation
│   ├── Phase4Generation.tsx     # Phase 4: Generation progress
│   └── Phase5Results.tsx        # Phase 5: Results and downloads
├── lib/
│   ├── api.ts              # API client and types
│   └── utils.ts            # Utility functions
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind configuration
├── tsconfig.json           # TypeScript configuration
└── next.config.js          # Next.js configuration
```

## 🎯 Workflow Phases

### Phase 1: Prompt Input
- User enters story prompt with validation
- Optional title and scene count selection
- Example prompts for inspiration
- Real-time character count

### Phase 2: Enhanced Story
- Display original vs enhanced story
- Enhancement details and statistics
- User can proceed or start over
- Processing time information

### Phase 3: Confirmation
- Summary of what will be generated
- Cost and time estimates
- Clear confirmation buttons
- Important notes and warnings

### Phase 4: Generation
- Real-time progress tracking
- Step-by-step generation status
- Estimated time remaining
- Visual progress indicators

### Phase 5: Results
- Complete story script display
- Download all generated files
- Generation statistics
- Option to create another video

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (#3b82f6 to #8b5cf6)
- **Success**: Green (#10b981)
- **Warning**: Orange (#f59e0b)
- **Error**: Red (#ef4444)
- **Neutral**: Gray scale

### Components
- **Cards**: Glassmorphism effect with backdrop blur
- **Buttons**: Gradient backgrounds with hover effects
- **Progress**: Animated progress bars
- **Icons**: Consistent Lucide React icons

### Animations
- **Page Transitions**: Fade in/out with slide effects
- **Component Loading**: Staggered animations
- **Progress Updates**: Smooth progress bar animations
- **Hover Effects**: Subtle scale and color transitions

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### API Configuration

The frontend is configured to communicate with the backend API at `http://localhost:8000`. You can change this by:

1. Setting the `NEXT_PUBLIC_API_URL` environment variable
2. Modifying the `API_BASE_URL` in `lib/api.ts`

### Tailwind Configuration

The Tailwind config includes:
- Custom color palette
- Custom animations
- Responsive breakpoints
- Component variants

## 📱 Responsive Design

The frontend is fully responsive with breakpoints:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

Key responsive features:
- Flexible grid layouts
- Mobile-first navigation
- Touch-friendly buttons
- Optimized typography

## 🔄 State Management

The application uses React's built-in state management:
- **useState**: For local component state
- **useEffect**: For side effects and API calls
- **Context**: For global state (if needed in future)

## 🚀 Deployment

### Build for Production

```bash
npm run build
# or
yarn build
```

### Start Production Server

```bash
npm start
# or
yarn start
```

### Deployment Options

1. **Vercel** (Recommended):
   ```bash
   npm install -g vercel
   vercel
   ```

2. **Netlify**:
   - Connect your repository
   - Build command: `npm run build`
   - Publish directory: `.next`

3. **Docker**:
   ```dockerfile
   FROM node:18-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   EXPOSE 3000
   CMD ["npm", "start"]
   ```

## 🧪 Testing

### Run Tests

```bash
npm run test
# or
yarn test
```

### Type Checking

```bash
npm run type-check
# or
yarn type-check
```

### Linting

```bash
npm run lint
# or
yarn lint
```

## 🔍 Development

### Code Style

- **TypeScript**: Strict mode enabled
- **ESLint**: Next.js recommended rules
- **Prettier**: Automatic code formatting
- **Conventional Commits**: For commit messages

### Component Guidelines

1. **Use TypeScript**: All components should be typed
2. **Follow Naming**: PascalCase for components, camelCase for functions
3. **Props Interface**: Define clear prop interfaces
4. **Error Boundaries**: Wrap components in error boundaries
5. **Loading States**: Always show loading states for async operations

### API Integration

The frontend communicates with the backend through the `workflowAPI` object in `lib/api.ts`. All API calls include:

- Error handling
- Loading states
- Type safety
- Retry logic (where appropriate)

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**:
   - Ensure backend server is running
   - Check `NEXT_PUBLIC_API_URL` environment variable
   - Verify CORS settings on backend

2. **Build Errors**:
   - Clear `.next` directory: `rm -rf .next`
   - Reinstall dependencies: `npm install`
   - Check TypeScript errors: `npm run type-check`

3. **Styling Issues**:
   - Ensure Tailwind CSS is properly configured
   - Check for conflicting CSS imports
   - Verify PostCSS configuration

### Debug Mode

Enable debug logging:

```bash
NODE_ENV=development DEBUG=* npm run dev
```

## 📈 Performance

### Optimization Features

- **Code Splitting**: Automatic with Next.js
- **Image Optimization**: Next.js Image component
- **Bundle Analysis**: `npm run analyze`
- **Lazy Loading**: Components loaded on demand
- **Caching**: API responses cached appropriately

### Performance Monitoring

- **Core Web Vitals**: Monitor with Lighthouse
- **Bundle Size**: Check with `npm run analyze`
- **API Response Times**: Monitor in browser dev tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Workflow

1. **Setup**: `npm install`
2. **Start Dev**: `npm run dev`
3. **Test**: `npm run test`
4. **Build**: `npm run build`
5. **Deploy**: Follow deployment instructions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation
- Contact the development team

---

**🎉 Happy Coding!** Build amazing video generation experiences with this modern Next.js frontend. 