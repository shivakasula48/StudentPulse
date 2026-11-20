from sqlalchemy.orm import Session
from app.models.models import (
    Skill, RoleSkillRequirement, AssessmentQuestion, LearningResource
)

SKILLS_DATA = [
    # Programming
    {"name": "Java", "category": "Programming", "description": "Core Java, OOP principles, JVM architecture"},
    {"name": "Python", "category": "Programming", "description": "Python syntax, standard library, scripting"},
    {"name": "JavaScript", "category": "Programming", "description": "ES6+, async programming, closures"},
    {"name": "TypeScript", "category": "Programming", "description": "Static typing, interfaces, generics for JS"},
    {"name": "C++", "category": "Programming", "description": "Pointers, memory management, STL"},
    {"name": "OOP", "category": "Programming", "description": "Object-Oriented Programming principles and design"},
    {"name": "Collections Framework", "category": "Programming", "description": "Java Collections, lists, sets, maps, queues"},

    # Data Structures & Algo
    {"name": "Data Structures and Algorithms", "category": "Computer Science", "description": "Arrays, Trees, Graphs, Sorting, DP, Big-O"},

    # Web Development
    {"name": "React", "category": "Web Development", "description": "React components, hooks, virtual DOM, state management"},
    {"name": "HTML/CSS", "category": "Web Development", "description": "Semantic HTML, responsive CSS, Flexbox, Grid"},
    {"name": "Node.js", "category": "Web Development", "description": "Server-side JavaScript runtime, event loop, NPM"},
    {"name": "REST APIs", "category": "Web Development", "description": "HTTP methods, status codes, API design, JSON"},

    # Databases
    {"name": "SQL", "category": "Database", "description": "Relational queries, aggregations, joins, subqueries"},
    {"name": "PostgreSQL", "category": "Database", "description": "Relational open-source DB, indexing, ACID transactions"},
    {"name": "MongoDB", "category": "Database", "description": "NoSQL document store, aggregation pipelines"},
    {"name": "JDBC", "category": "Database", "description": "Java Database Connectivity API"},

    # Frameworks
    {"name": "Spring Boot", "category": "Framework", "description": "Enterprise Java backend framework, dependency injection"},
    {"name": "FastAPI", "category": "Framework", "description": "Modern high-performance Python async web framework"},
    {"name": "Django", "category": "Framework", "description": "Batteries-included full-stack Python web framework"},

    # Tools & DevOps
    {"name": "Git and GitHub", "category": "Tools", "description": "Version control, branching, pull requests, collaboration"},
    {"name": "Docker", "category": "Tools", "description": "Containerization, Dockerfile, multi-container orchestration"},
    {"name": "Linux/Bash", "category": "Tools", "description": "Command line, shell scripting, file permissions"},

    # AI & Data
    {"name": "Machine Learning", "category": "AI/ML", "description": "Supervised, unsupervised learning, model evaluation"},
    {"name": "Deep Learning", "category": "AI/ML", "description": "Neural networks, PyTorch/TensorFlow, backpropagation"},
    {"name": "Data Analysis", "category": "AI/ML", "description": "Data wrangling, Pandas, NumPy, visualization"},

    # Professional / Soft Skills
    {"name": "Communication", "category": "Professional Skills", "description": "Clear verbal and written technical communication"},
    {"name": "Problem Solving", "category": "Professional Skills", "description": "Analytical reasoning and debugging methodologies"},
    {"name": "Teamwork", "category": "Professional Skills", "description": "Collaboration, code reviews, agile teamwork"},
    {"name": "Time Management", "category": "Professional Skills", "description": "Prioritization, task estimation, delivery focus"}
]

ROLE_REQUIREMENTS_DATA = {
    "Java Developer": [
        ("Java", "Advanced", "Critical"),
        ("OOP", "Advanced", "Critical"),
        ("Collections Framework", "Intermediate", "High"),
        ("Data Structures and Algorithms", "Intermediate", "Critical"),
        ("SQL", "Intermediate", "High"),
        ("JDBC", "Intermediate", "Medium"),
        ("Spring Boot", "Intermediate", "Critical"),
        ("REST APIs", "Intermediate", "High"),
        ("Git and GitHub", "Intermediate", "Medium"),
    ],
    "Python Developer": [
        ("Python", "Advanced", "Critical"),
        ("OOP", "Intermediate", "High"),
        ("Data Structures and Algorithms", "Intermediate", "Critical"),
        ("SQL", "Intermediate", "High"),
        ("FastAPI", "Intermediate", "High"),
        ("REST APIs", "Intermediate", "High"),
        ("Git and GitHub", "Intermediate", "Medium"),
        ("Docker", "Beginner", "Medium"),
    ],
    "Full Stack Developer": [
        ("JavaScript", "Advanced", "Critical"),
        ("React", "Intermediate", "Critical"),
        ("Node.js", "Intermediate", "High"),
        ("SQL", "Intermediate", "High"),
        ("REST APIs", "Advanced", "Critical"),
        ("HTML/CSS", "Advanced", "High"),
        ("Git and GitHub", "Intermediate", "Medium"),
        ("Docker", "Beginner", "Medium"),
    ],
    "Frontend Developer": [
        ("JavaScript", "Advanced", "Critical"),
        ("React", "Advanced", "Critical"),
        ("HTML/CSS", "Advanced", "Critical"),
        ("TypeScript", "Intermediate", "High"),
        ("REST APIs", "Intermediate", "High"),
        ("Git and GitHub", "Intermediate", "Medium"),
    ],
    "Backend Developer": [
        ("Python", "Intermediate", "High"),
        ("SQL", "Advanced", "Critical"),
        ("PostgreSQL", "Intermediate", "High"),
        ("REST APIs", "Advanced", "Critical"),
        ("Docker", "Intermediate", "High"),
        ("Data Structures and Algorithms", "Intermediate", "High"),
        ("Git and GitHub", "Intermediate", "Medium"),
    ],
    "Data Analyst": [
        ("SQL", "Advanced", "Critical"),
        ("Python", "Intermediate", "High"),
        ("Data Analysis", "Advanced", "Critical"),
        ("PostgreSQL", "Intermediate", "Medium"),
        ("Problem Solving", "Advanced", "High"),
        ("Communication", "Intermediate", "Medium"),
    ],
    "AI/ML Engineer": [
        ("Python", "Advanced", "Critical"),
        ("Machine Learning", "Advanced", "Critical"),
        ("Data Structures and Algorithms", "Intermediate", "High"),
        ("Deep Learning", "Intermediate", "High"),
        ("Data Analysis", "Intermediate", "High"),
        ("Git and GitHub", "Intermediate", "Medium"),
    ],
    "Software Engineer": [
        ("Data Structures and Algorithms", "Advanced", "Critical"),
        ("OOP", "Advanced", "Critical"),
        ("SQL", "Intermediate", "High"),
        ("Git and GitHub", "Intermediate", "High"),
        ("Problem Solving", "Advanced", "Critical"),
        ("Teamwork", "Intermediate", "Medium"),
    ],
}

ASSESSMENT_QUESTIONS_DATA = [
    # 1. Programming Skills
    {
        "category": "Programming Skills",
        "skill_name": "Java",
        "difficulty": "Intermediate",
        "question_text": "In Java, what is the key difference between StringBuffer and StringBuilder?",
        "option_a": "StringBuffer is synchronized and thread-safe, whereas StringBuilder is not.",
        "option_b": "StringBuilder is synchronized, whereas StringBuffer is faster.",
        "option_c": "StringBuffer is immutable, while StringBuilder is mutable.",
        "option_d": "There is no difference in concurrency or performance.",
        "correct_option": "A",
        "explanation": "StringBuffer methods are synchronized, making it thread-safe at a slight performance cost. StringBuilder is non-synchronized and faster for single-threaded usage."
    },
    {
        "category": "Programming Skills",
        "skill_name": "OOP",
        "difficulty": "Intermediate",
        "question_text": "Which OOP principle is primarily demonstrated when a subclass provides a specific implementation of a method defined in its superclass?",
        "option_a": "Encapsulation",
        "option_b": "Method Overriding (Polymorphism)",
        "option_c": "Data Hiding",
        "option_d": "Aggregation",
        "correct_option": "B",
        "explanation": "Runtime polymorphism (dynamic method dispatch) is achieved through method overriding in subclasses."
    },
    {
        "category": "Programming Skills",
        "skill_name": "Python",
        "difficulty": "Intermediate",
        "question_text": "In Python, how does a generator function differ from a regular function?",
        "option_a": "Generators return a list immediately.",
        "option_b": "Generators use the yield statement to produce items lazily on demand.",
        "option_c": "Generators cannot accept arguments.",
        "option_d": "Generators execute in a separate C thread.",
        "correct_option": "B",
        "explanation": "The yield keyword pauses function execution and maintains state, generating items one at a time to conserve memory."
    },
    {
        "category": "Programming Skills",
        "skill_name": "Collections Framework",
        "difficulty": "Intermediate",
        "question_text": "Which Java Collection class implements a hash table and does NOT allow null keys or null values?",
        "option_a": "HashMap",
        "option_b": "TreeMap",
        "option_c": "Hashtable / ConcurrentHashMap",
        "option_d": "LinkedHashMap",
        "correct_option": "C",
        "explanation": "Hashtable and ConcurrentHashMap prohibit null keys and null values to avoid ambiguous lookups in multi-threaded environments."
    },

    # 2. Data Structures and Algorithms
    {
        "category": "Data Structures and Algorithms",
        "skill_name": "Data Structures and Algorithms",
        "difficulty": "Intermediate",
        "question_text": "What is the average time complexity of searching an element in a balanced Binary Search Tree (AVL or Red-Black Tree)?",
        "option_a": "O(1)",
        "option_b": "O(log N)",
        "option_c": "O(N)",
        "option_d": "O(N log N)",
        "correct_option": "B",
        "explanation": "A self-balancing BST maintains height proportional to log(N), guaranteeing O(log N) search, insertion, and deletion."
    },
    {
        "category": "Data Structures and Algorithms",
        "skill_name": "Data Structures and Algorithms",
        "difficulty": "Advanced",
        "question_text": "Which algorithm is most suitable for finding the shortest path between all pairs of vertices in a weighted graph with negative edges but no negative cycles?",
        "option_a": "Dijkstra's Algorithm",
        "option_b": "Floyd-Warshall Algorithm",
        "option_c": "Kruskal's Algorithm",
        "option_d": "Prim's Algorithm",
        "correct_option": "B",
        "explanation": "Floyd-Warshall is a dynamic programming algorithm with O(V^3) time complexity designed for all-pairs shortest paths and handles negative edges."
    },
    {
        "category": "Data Structures and Algorithms",
        "skill_name": "Data Structures and Algorithms",
        "difficulty": "Beginner",
        "question_text": "Which data structure operates on a Last In, First Out (LIFO) order?",
        "option_a": "Queue",
        "option_b": "PriorityQueue",
        "option_c": "Stack",
        "option_d": "Deque",
        "correct_option": "C",
        "explanation": "A stack pushes and pops elements from the top, making it LIFO."
    },

    # 3. Database Management
    {
        "category": "Database Management",
        "skill_name": "SQL",
        "difficulty": "Intermediate",
        "question_text": "What is the primary difference between WHERE and HAVING clauses in SQL?",
        "option_a": "WHERE filters rows before grouping; HAVING filters groups after GROUP BY aggregation.",
        "option_b": "HAVING is faster than WHERE on indexed columns.",
        "option_c": "WHERE works with aggregate functions like COUNT(), while HAVING cannot.",
        "option_d": "There is no functional difference.",
        "correct_option": "A",
        "explanation": "WHERE filters individual table rows prior to aggregation, while HAVING filters aggregated group results."
    },
    {
        "category": "Database Management",
        "skill_name": "PostgreSQL",
        "difficulty": "Intermediate",
        "question_text": "In relational database ACID properties, what does 'Isolation' guarantee?",
        "option_a": "Transactions are completely saved even if hardware loses power.",
        "option_b": "Concurrent execution of transactions leaves the database in the same state as if executed serially.",
        "option_c": "Foreign key constraints are enforced unconditionally.",
        "option_d": "All changes within a transaction either succeed or fail as a single unit.",
        "correct_option": "B",
        "explanation": "Isolation prevents concurrent transactions from interfering with each other's intermediate state."
    },
    {
        "category": "Database Management",
        "skill_name": "JDBC",
        "difficulty": "Intermediate",
        "question_text": "Why should PreparedStatement be favored over Statement in JDBC for executing queries with dynamic parameters?",
        "option_a": "PreparedStatement executes on the client machine instead of the DB server.",
        "option_b": "PreparedStatement precompiles SQL and prevents SQL injection via parameterized queries.",
        "option_c": "PreparedStatement does not require a database connection.",
        "option_d": "Statement does not support SELECT queries.",
        "correct_option": "B",
        "explanation": "PreparedStatement separates SQL logic from data parameters, eliminating SQL injection vulnerabilities and allowing DB statement caching."
    },

    # 4. Web Development
    {
        "category": "Web Development",
        "skill_name": "React",
        "difficulty": "Intermediate",
        "question_text": "In React, what is the primary purpose of the useEffect hook dependency array?",
        "option_a": "To register CSS animations.",
        "option_b": "To control when the effect function executes based on changes in specified dependencies.",
        "option_c": "To bind this context to event handlers.",
        "option_d": "To force synchronous server-side rendering.",
        "correct_option": "B",
        "explanation": "React compares values in the dependency array across renders using Object.is and skips running the effect if no values have changed."
    },
    {
        "category": "Web Development",
        "skill_name": "REST APIs",
        "difficulty": "Intermediate",
        "question_text": "Which HTTP method is considered idempotent and used to replace an entire existing resource representation?",
        "option_a": "POST",
        "option_b": "PUT",
        "option_c": "PATCH",
        "option_d": "CONNECT",
        "correct_option": "B",
        "explanation": "PUT is idempotent: executing it multiple times with the same body results in the exact same resource state."
    },
    {
        "category": "Web Development",
        "skill_name": "Spring Boot",
        "difficulty": "Intermediate",
        "question_text": "What does the @RestController annotation in Spring Boot combine?",
        "option_a": "@Controller and @ResponseBody",
        "option_b": "@Service and @Repository",
        "option_c": "@Component and @Autowired",
        "option_d": "@Configuration and @Bean",
        "correct_option": "A",
        "explanation": "@RestController is a convenience annotation combining @Controller and @ResponseBody, ensuring response objects are serialized directly into JSON/XML."
    },

    # 5. Software Engineering
    {
        "category": "Software Engineering",
        "skill_name": "Git and GitHub",
        "difficulty": "Intermediate",
        "question_text": "What does 'git rebase' do when integrating changes from a feature branch into the main branch?",
        "option_a": "It deletes all commits and leaves uncommitted files in working directory.",
        "option_b": "It reapplies commits from the current branch on top of another base commit, creating a linear history.",
        "option_c": "It always creates a new 3-way merge commit with two parents.",
        "option_d": "It reverts all unstaged local edits.",
        "correct_option": "B",
        "explanation": "Rebase rewrites commit history by transplanting branch commits on top of the target base tip for a cleaner linear log."
    },
    {
        "category": "Software Engineering",
        "skill_name": "Problem Solving",
        "difficulty": "Intermediate",
        "question_text": "Which design pattern is best suited for defining a family of interchangeable algorithms that can vary independently from clients that use them?",
        "option_a": "Singleton Pattern",
        "option_b": "Strategy Pattern",
        "option_c": "Decorator Pattern",
        "option_d": "Observer Pattern",
        "correct_option": "B",
        "explanation": "The Strategy pattern encapsulates algorithmic variations into separate classes conforming to a common interface."
    },

    # 6. Artificial Intelligence / Machine Learning
    {
        "category": "Artificial Intelligence / Machine Learning",
        "skill_name": "Machine Learning",
        "difficulty": "Intermediate",
        "question_text": "Which technique is specifically used to prevent overfitting in machine learning models by penalizing large parameter weights?",
        "option_a": "One-Hot Encoding",
        "option_b": "Regularization (L1 Lasso / L2 Ridge)",
        "option_c": "Label Binarization",
        "option_d": "MinMax Feature Scaling",
        "correct_option": "B",
        "explanation": "L1 (Lasso) and L2 (Ridge) add penalty terms to the loss function proportional to parameter magnitudes, constraining model complexity."
    },
    {
        "category": "Artificial Intelligence / Machine Learning",
        "skill_name": "Data Analysis",
        "difficulty": "Intermediate",
        "question_text": "When evaluating an imbalanced classification model (e.g. 99% negative class), why is raw Accuracy a misleading metric?",
        "option_a": "Accuracy is slower to calculate than F1-score.",
        "option_b": "A trivial model predicting the majority class all the time can achieve 99% accuracy while detecting zero positives.",
        "option_c": "Accuracy cannot be computed for binary outcomes.",
        "option_d": "Scikit-learn does not support accuracy.",
        "correct_option": "B",
        "explanation": "In skewed datasets, high accuracy is trivially achieved by classifying everything as the majority class; Precision, Recall, and PR-AUC are required."
    },

    # 7. Communication Skills
    {
        "category": "Communication Skills",
        "skill_name": "Communication",
        "difficulty": "Intermediate",
        "question_text": "When presenting a software architectural decision to non-technical business stakeholders, what is the most effective approach?",
        "option_a": "Focus strictly on internal data structure complexity and pointer arithmetic.",
        "option_b": "Frame the decision in terms of business impact, cost efficiency, user experience, and risk reduction.",
        "option_c": "Present 50 slides of unformatted source code.",
        "option_d": "Avoid mentioning trade-offs or constraints.",
        "correct_option": "B",
        "explanation": "Effective professional communication translates technical trade-offs into tangible business objectives and value for non-technical stakeholders."
    },
    {
        "category": "Communication Skills",
        "skill_name": "Teamwork",
        "difficulty": "Intermediate",
        "question_text": "What is the best practice when conducting a constructive code review on a peer's pull request?",
        "option_a": "Point out shortcomings aggressively without explaining alternative solutions.",
        "option_b": "Focus on the code quality and logic, explain the rationale behind suggestions, and highlight good work.",
        "option_c": "Approve immediately without reading the diff to save team time.",
        "option_d": "Demand full architectural redesigns on minor bug fixes.",
        "correct_option": "B",
        "explanation": "Constructive code reviews foster technical rigor and mutual trust by focusing objectively on code design, security, and actionable improvements."
    },

    # 8. Problem-Solving
    {
        "category": "Problem-Solving",
        "skill_name": "Problem Solving",
        "difficulty": "Intermediate",
        "question_text": "When debugging an elusive production issue that only occurs intermittently under high load, what is the recommended first step?",
        "option_a": "Immediately push untested code changes directly to production.",
        "option_b": "Analyze application and server logs, gather telemetry metrics, and reproduce the concurrent conditions in a staging environment.",
        "option_c": "Delete the production database and start fresh.",
        "option_d": "Blame the operating system without investigating.",
        "correct_option": "B",
        "explanation": "Systematic root-cause analysis relies on evidence, log correlation, metric analysis, and reproducible test conditions before applying fixes."
    }
]

LEARNING_RESOURCES_DATA = [
    # Java & Spring
    {
        "title": "Oracle Official Java Documentation & Tutorials",
        "skill_category": "Java",
        "resource_type": "Documentation",
        "url": "https://docs.oracle.com/en/java/",
        "difficulty": "Beginner to Advanced",
        "description": "The definitive specification, guides, and tutorials for the Java Platform."
    },
    {
        "title": "Spring Boot Reference Documentation",
        "skill_category": "Spring Boot",
        "resource_type": "Documentation",
        "url": "https://docs.spring.io/spring-boot/docs/current/reference/html/",
        "difficulty": "Intermediate",
        "description": "Comprehensive reference guide for building production-grade Spring Boot applications."
    },
    {
        "title": "Baeldung: Spring Boot and Java Guides",
        "skill_category": "Spring Boot",
        "resource_type": "Tutorials",
        "url": "https://www.baeldung.com/",
        "difficulty": "Intermediate",
        "description": "In-depth tutorials covering Spring Framework, Spring Security, REST APIs, and Java Collections."
    },

    # Python & FastAPI
    {
        "title": "Python Official Documentation & Tutorial",
        "skill_category": "Python",
        "resource_type": "Documentation",
        "url": "https://docs.python.org/3/tutorial/",
        "difficulty": "Beginner to Advanced",
        "description": "Official Python 3 tutorial detailing data structures, modules, classes, and standard libraries."
    },
    {
        "title": "FastAPI Official Interactive Tutorial",
        "skill_category": "FastAPI",
        "resource_type": "Documentation",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "difficulty": "Intermediate",
        "description": "Step-by-step interactive documentation for building modern APIs with Pydantic and OpenAPI."
    },

    # Web & React
    {
        "title": "React Official Documentation (react.dev)",
        "skill_category": "React",
        "resource_type": "Documentation",
        "url": "https://react.dev/",
        "difficulty": "Beginner to Intermediate",
        "description": "Interactive, modern guide to thinking in React, state management, and custom hooks."
    },
    {
        "title": "MDN Web Docs: Modern JavaScript (ES6+)",
        "skill_category": "JavaScript",
        "resource_type": "Documentation",
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        "difficulty": "Beginner to Advanced",
        "description": "Authoritative guide to JavaScript language features, DOM manipulation, and asynchronous programming."
    },

    # Database
    {
        "title": "PostgreSQL Official Documentation",
        "skill_category": "PostgreSQL",
        "resource_type": "Documentation",
        "url": "https://www.postgresql.org/docs/",
        "difficulty": "Intermediate",
        "description": "Detailed manual covering SQL syntax, indexing, schema design, and performance tuning."
    },
    {
        "title": "SQLBolt - Interactive SQL Lessons",
        "skill_category": "SQL",
        "resource_type": "Coding practice",
        "url": "https://sqlbolt.com/",
        "difficulty": "Beginner",
        "description": "Interactive in-browser exercises to practice SELECT, JOIN, GROUP BY, and data modifications."
    },

    # DSA & Problem Solving
    {
        "title": "NeetCode DSA Roadmap & Patterns",
        "skill_category": "Data Structures and Algorithms",
        "resource_type": "Coding practice",
        "url": "https://neetcode.io/roadmap",
        "difficulty": "Intermediate to Advanced",
        "description": "Structured curriculum covering two pointers, sliding window, binary search, trees, and dynamic programming."
    },
    {
        "title": "Git Official Pro Git Book",
        "skill_category": "Git and GitHub",
        "resource_type": "Documentation",
        "url": "https://git-scm.com/book/en/v2",
        "difficulty": "Beginner to Intermediate",
        "description": "Complete guide to version control, branching strategies, and internal object storage."
    }
]

def seed_database(db: Session):
    """Seed base skills, role requirements, questions, and resources if empty."""
    # 1. Seed Skills
    existing_skills_count = db.query(Skill).count()
    skill_map = {}
    if existing_skills_count == 0:
        for s in SKILLS_DATA:
            skill = Skill(name=s["name"], category=s["category"], description=s["description"])
            db.add(skill)
        db.commit()
    
    # Reload skills into map
    for skill in db.query(Skill).all():
        skill_map[skill.name] = skill.id

    # 2. Seed Role Requirements
    existing_roles_count = db.query(RoleSkillRequirement).count()
    if existing_roles_count == 0:
        for role_name, reqs in ROLE_REQUIREMENTS_DATA.items():
            for skill_name, required_level, priority in reqs:
                if skill_name in skill_map:
                    role_req = RoleSkillRequirement(
                        role_name=role_name,
                        skill_id=skill_map[skill_name],
                        required_level=required_level,
                        priority=priority
                    )
                    db.add(role_req)
        db.commit()

    # 3. Seed Assessment Questions
    existing_q_count = db.query(AssessmentQuestion).count()
    if existing_q_count == 0:
        for q in ASSESSMENT_QUESTIONS_DATA:
            question = AssessmentQuestion(
                category=q["category"],
                skill_name=q["skill_name"],
                difficulty=q["difficulty"],
                question_text=q["question_text"],
                option_a=q["option_a"],
                option_b=q["option_b"],
                option_c=q["option_c"],
                option_d=q["option_d"],
                correct_option=q["correct_option"],
                explanation=q["explanation"]
            )
            db.add(question)
        db.commit()

    # 4. Seed Learning Resources
    existing_res_count = db.query(LearningResource).count()
    if existing_res_count == 0:
        for r in LEARNING_RESOURCES_DATA:
            resource = LearningResource(
                title=r["title"],
                skill_category=r["skill_category"],
                resource_type=r["resource_type"],
                url=r["url"],
                difficulty=r["difficulty"],
                description=r["description"]
            )
            db.add(resource)
        db.commit()
