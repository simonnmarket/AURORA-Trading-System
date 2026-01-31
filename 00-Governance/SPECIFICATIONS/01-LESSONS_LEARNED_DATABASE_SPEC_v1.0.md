# Lessons Learned Database Structure Spec  
**Version**: 1.0  
**Date**: 2026-01-31 16:00:37  

## Introduction  
The purpose of this document is to outline the database structure for the Lessons Learned Database for the AURORA Trading System project. This database will be used to store and manage lessons learned during the project lifecycle, facilitating knowledge sharing and continuous improvement.  

## Database Structure  
The Lessons Learned Database will consist of the following tables:  
1. **Lessons**  
   - **ID**: Unique identifier for each lesson (Primary Key)  
   - **Title**: Brief title of the lesson learned  
   - **Description**: Detailed description of the lesson learned  
   - **Date Captured**: Date when the lesson was captured  
   - **Project Phase**: Phase of the project during which the lesson was learned (e.g., Initiation, Planning, Execution, etc.)  
   - **Staff Involved**: Names/IDs of the staff members involved in the lesson  

2. **Categories**  
   - **ID**: Unique identifier for each category (Primary Key)  
   - **Category Name**: Name of the category (e.g., Technical, Process, Team Management, etc.)  

3. **Lesson Categories**  
   - **Lesson ID**: Identifier for the lesson (Foreign Key to Lessons table)  
   - **Category ID**: Identifier for the category (Foreign Key to Categories table)  

## Relationships  
- Each lesson can belong to multiple categories through the Lesson Categories table.  
- Each category can be associated with multiple lessons.  

## Conclusion  
This structure will allow for efficient tracking, categorization, and retrieval of lessons learned, thereby enhancing project outcomes and future learning. Further updates to this specification will be made as the project evolves.  

---  
**Prepared by**: simonnmarket  
**Date**: 2026-01-31 16:00:37