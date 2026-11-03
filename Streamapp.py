import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="Programming Code Viewer",
    page_icon="💻",
    layout="wide"
)

# 2. Local Fallback Database (Ensures the app ALWAYS functions)
MOCK_PROGRAMMING_POSTS = [
    {
        "title": "Mastering List Comprehensions in Python 3",
        "user": {"name": "Alex Pythonista"},
        "readable_publish_date": "Nov 3",
        "tag_list": ["python", "programming", "clean-code"],
        "description": "Learn how to write elegant, memory-efficient list comprehensions. This guide breaks down filtering, nested loops, and formatting best practices for modern developers.",
        "url": "https://dev.to",
        "cover_image": "https://unsplash.com"
    },
    {
        "title": "Understanding JavaScript Closures and Scope",
        "user": {"name": "Sarah Dev"},
        "readable_publish_date": "Oct 29",
        "tag_list": ["javascript", "webdev", "programming"],
        "description": "Closures are one of the most powerful features of JavaScript. Dive deep into lexical scoping, execution contexts, and practical patterns for protecting private data variables.",
        "url": "https://dev.to",
        "cover_image": "https://unsplash.com"
    },
    {
        "title": "Why Rust is Dominating Modern Systems Programming",
        "user": {"name": "Ferris Coder"},
        "readable_publish_date": "Oct 25",
        "tag_list": ["rust", "programming", "backend"],
        "description": "Memory safety without a garbage collector. Discover how Rust uses its strict borrow checker rules to eliminate data races and segment faults at compile time.",
        "url": "https://dev.to",
        "cover_image": "https://unsplash.com"
    }
]

# 3. Crash-Proof Programming API Fetch Function
@st.cache_data(ttl=600)
def fetch_programming_posts(tag="programming", per_page=15):
    url = "https://dev.to/api/articles"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    params = {
        "per_page": per_page,
        "tag": tag.lower()
    }
        
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status() 
        
        # Test if it can parse as JSON safely
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return data
        raise ValueError("Empty or structured invalid response format")
        
    except Exception:
        # Silently load mock fallback data so the interface user experiences zero down-time
        return [p for p in MOCK_PROGRAMMING_POSTS if tag == "programming" or tag in p["tag_list"]]

# 4. Sidebar UI Restricted Exclusively to Languages & Frameworks
st.sidebar.title("💻 Programming Languages")
category_options = ["All Programming", "Python", "JavaScript", "Rust"]
selected_category = st.sidebar.selectbox("Select a language:", category_options)
post_count = st.sidebar.slider("Number of blogs to load:", min_value=5, max_value=30, value=15, step=5)

# 5. Process Category Selection Mapping
target_tag = "programming" if selected_category == "All Programming" else selected_category.lower()

# 6. Fetch the Data
posts = fetch_programming_posts(tag=target_tag, per_page=post_count)

# 7. Main Layout UI
st.title("💻 Developer Central: Programming Feed")

if not posts:
    st.info("No active programming blogs found matching this language tag.")
else:
    col_list, col_view = st.columns([1, 2], gap="medium")
    
    with col_list:
        st.subheader("📬 Code Articles")
        options_map = {f"📝 {p['title']}": idx for idx, p in enumerate(posts)}
        
        selected_display_title = st.radio(
            "Select an article to view:",
            options=list(options_map.keys()),
            label_visibility="collapsed"
        )
        
        selected_index = options_map[selected_display_title]
        selected_post = posts[selected_index]
        
    with col_view:
        st.subheader("📖 Code Reader Pane")
        st.divider()
        
        if selected_post.get("cover_image"):
            st.image(selected_post["cover_image"], width="stretch")
            
        st.title(selected_post["title"])
        
        # Metadata
        meta_col1, meta_col2 = st.columns(2)
        with meta_col1:
            st.caption(f"👤 **Developer:** {selected_post['user']['name']}")
        with meta_col2:
            st.caption(f"🗓 Honor Date: {selected_post['readable_publish_date']}")
            
        # Display Tags
        tags_str = " ".join([f"`#{t}`" for t in selected_post.get("tag_list", [])])
        st.markdown(f"🏷️ **Tags:** {tags_str}")
        
        st.write(selected_post.get("description", "No description available."))
        st.link_button("🌐 Open Source Post Context", selected_post["url"])
