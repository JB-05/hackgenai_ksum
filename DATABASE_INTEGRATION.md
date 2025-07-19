# 🗄️ Database Integration Guide

## 📊 **Current System Analysis**

### **What You Have Now:**
- ✅ **File Storage**: Organized `save_outputs/` directory
- ❌ **In-Memory Workflows**: Data lost on server restart
- ❌ **No Persistence**: No metadata tracking
- ❌ **No User Management**: No session tracking

### **What Database Adds:**
- ✅ **Persistence**: Workflow data survives restarts
- ✅ **File Tracking**: Metadata for all generated files
- ✅ **User Management**: Future user accounts
- ✅ **Cost Monitoring**: API usage tracking
- ✅ **Analytics**: Usage statistics and insights

---

## 🎯 **Database Options**

### **Option 1: SQLite (Recommended for MVP)**
**Pros:**
- ✅ Zero setup required
- ✅ Single file database
- ✅ Built into Python
- ✅ Perfect for development/prototyping
- ✅ Easy to backup and migrate

**Cons:**
- ❌ Limited concurrent users
- ❌ No built-in user management
- ❌ File size limitations

**Best for:** Development, small-scale deployment, MVP

### **Option 2: PostgreSQL (Production Ready)**
**Pros:**
- ✅ Enterprise-grade reliability
- ✅ Excellent concurrent user support
- ✅ Advanced features (JSON, full-text search)
- ✅ Built-in user management
- ✅ Scalable

**Cons:**
- ❌ Requires setup and maintenance
- ❌ More complex deployment
- ❌ Additional dependencies

**Best for:** Production deployment, high-traffic applications

### **Option 3: MongoDB (Document Store)**
**Pros:**
- ✅ Flexible schema
- ✅ Good for JSON-like data
- ✅ Easy to scale horizontally
- ✅ Built-in file storage (GridFS)

**Cons:**
- ❌ Less ACID compliance
- ❌ More complex queries
- ❌ Additional setup required

**Best for:** Document-heavy applications, rapid prototyping

---

## 🚀 **Quick Start: SQLite Integration**

### **Step 1: Install Dependencies**
```bash
# SQLite is built into Python, no additional installation needed
```

### **Step 2: Initialize Database**
```python
# The database will be automatically created when you import the module
from api.database import db_manager
```

### **Step 3: Update Workflow Manager**
```python
# In workflow_manager.py, add database calls:

from .database import db_manager

class WorkflowManager:
    def create_workflow(self) -> str:
        workflow_id = str(uuid.uuid4())
        
        # Create in-memory workflow
        self.active_workflows[workflow_id] = WorkflowStatus(...)
        
        # Add to database
        db_manager.create_workflow(workflow_id, "Original prompt", "Story title")
        
        return workflow_id
```

### **Step 4: Track Generated Files**
```python
# In each generation module, add file tracking:

# After generating an image
db_manager.add_generated_file(
    workflow_id=workflow_id,
    file_type="image",
    file_path="/files/images/scene_1.png",
    file_name="scene_1.png",
    file_size=1024000,
    metadata={"scene_number": 1, "style": "realistic"}
)
```

---

## 📈 **Database Schema Overview**

### **Core Tables:**

1. **`workflows`** - Main workflow tracking
   - Workflow ID, phases, status, timestamps
   - Original prompt and enhanced story

2. **`generated_files`** - All generated assets
   - File paths, sizes, metadata
   - Links to workflows

3. **`scenes`** - Scene breakdowns
   - Scene descriptions and prompts
   - Links to generated images

4. **`api_usage`** - Cost monitoring
   - API calls, tokens used, costs
   - Performance tracking

5. **`users`** - Future user management
   - User accounts and sessions

---

## 🔧 **Integration Steps**

### **Phase 1: Basic Integration (1-2 hours)**
1. ✅ **Database Schema**: Already created
2. ✅ **Database Manager**: Already created
3. 🔄 **Update Workflow Manager**: Add database calls
4. 🔄 **Update File Generation**: Track generated files
5. 🔄 **Add API Endpoints**: Database-backed endpoints

### **Phase 2: Enhanced Features (2-3 hours)**
1. 🔄 **User Management**: Basic user accounts
2. 🔄 **File Management**: Database-backed file operations
3. 🔄 **Analytics Dashboard**: Usage statistics
4. 🔄 **Cleanup Jobs**: Automatic old data cleanup

### **Phase 3: Production Features (3-4 hours)**
1. 🔄 **Backup System**: Automated database backups
2. 🔄 **Migration Scripts**: Schema updates
3. 🔄 **Performance Optimization**: Indexes and queries
4. 🔄 **Monitoring**: Database health monitoring

---

## 💡 **Recommendations**

### **For Your Current Stage:**
**✅ Use SQLite** - It's perfect for your current needs:
- Zero setup required
- Immediate persistence
- Easy to migrate later
- Perfect for development and MVP

### **When to Upgrade:**
- **PostgreSQL**: When you have >100 concurrent users
- **MongoDB**: When you need flexible document storage
- **Cloud Database**: When you deploy to production

### **Implementation Priority:**
1. **High**: Basic workflow persistence
2. **High**: File tracking and metadata
3. **Medium**: API usage monitoring
4. **Low**: User management system

---

## 🎯 **Next Steps**

1. **Test SQLite Integration**: Add database calls to existing workflow
2. **Verify File Tracking**: Ensure all generated files are tracked
3. **Add Analytics**: Monitor API usage and costs
4. **Plan Migration**: Consider PostgreSQL for production

**The database will significantly improve your system's reliability and provide valuable insights into usage patterns!** 🚀 