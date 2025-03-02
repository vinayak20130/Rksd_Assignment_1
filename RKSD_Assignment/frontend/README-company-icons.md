# Company Icons for Job Cards

This feature allows each job card to display a unique company icon (PNG image) instead of a generic icon.

## Current Implementation

The job cards now use company icons directly from the assets folder. The icons are imported and mapped in the JobCard component:

```javascript
// Import company icons from assets
import designerIcon from '@/assets/designer.png'
import growthManagerIcon from '@/assets/growthmanger.png'
import financialAnalystIcon from '@/assets/financialanalyst.png'
import securityAnalystIcon from '@/assets/securityanalyst.png'

// Map of company icons
const companyIconMap = {
  'designer': designerIcon,
  'growth-manager': growthManagerIcon,
  'financial-analyst': financialAnalystIcon,
  'security-analyst': securityAnalystIcon
}
```

## Using Company Icons in Job Cards

In your job data, include a `companyIcon` property with the key that matches the mapping in the JobCard component:

```javascript
const jobs = [
  {
    id: 1,
    title: 'Sr. UX Designer',
    // ... other job properties ...
    companyIcon: 'designer'
  }
]
```

## Adding New Company Icons

To add a new company icon:

1. Add the PNG image to the `src/assets` folder with a descriptive filename
   - Recommended size: 32x32 pixels
   - Transparent background works best

2. Import the new icon in the JobCard component:
   ```javascript
   import newCompanyIcon from '@/assets/new-company.png'
   ```

3. Add it to the companyIconMap:
   ```javascript
   const companyIconMap = {
     // ... existing icons ...
     'new-company': newCompanyIcon
   }
   ```

4. Use the new key in your job data:
   ```javascript
   {
     // ... other job properties ...
     companyIcon: 'new-company'
   }
   ```

## Benefits of Using Assets

- Better build optimization with Vite's asset handling
- Type safety with imports
- No need for runtime file existence checks
- Assets are properly hashed for cache busting in production builds 