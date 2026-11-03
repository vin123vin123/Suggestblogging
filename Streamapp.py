import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="Programming Code Viewer",
    page_icon="💻",
    layout="wide"
)

# 2. Strict Programming API Fetch Function
@st.cache_data(ttl=600)  # Caches results for 10 minutes
def fetch_programming_posts(tag="programming", per_page=15):
    url = "https://dev.to"
    # Fallback to general 'programming' if no specific sub-tag is chosen
    api_tag = tag if tag else "programming"
    params = {
        "per_page": per_page,
        "tag": api_tag.lower()
    }
        
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data from API. Status code: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# 3. Sidebar UI Restricted Exclusively to Languages & Frameworks
st.sidebar.title("💻 Programming Languages")
category_options = [
    "All Programming", 
    "Python", 
    "JavaScript", 
    "Go", 
    "Rust", 
    "Cpp", 
    "Java", 
    "TypeScript"
]
selected_category = st.sidebar.selectbox("Select a language:", category_options)
post_count = st.sidebar.slider("Number of blogs to load:", min_value=5, max_value=30, value=15, step=5)

# 4. Process Category Selection Mapping
if selected_category == "All Programming":
    target_tag = "programming"
else:
    target_tag = selected_category.lower()

# 5. Fetch the Filtered Programming Data
with st.spinner(f"Loading latest #{target_tag} articles..."):
    posts = fetch_programming_posts(tag=target_tag, per_page=post_count)

# 6. Main Layout UI
st.title("💻 Developer Central: Programming Feed")
st.markdown(f"Displaying real-time public articles restricted to **#{target_tag}**.")

if not posts:
    st.info("No active programming blogs found matching this language tag.")
else:
    # Double Column Layout
    col_list, col_view = st.columns([2, 3], gap="medium")
    
    with col_list:
        st.subheader("📬 Code Articles")
        
        # Clean dictionary map formatting for radio buttons
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
            st.image(selected_post["cover_image"], use_container_width=True)
            
        st.title(selected_post["title"])
        
        # Metadata
        meta_col1, meta_col2 = st.columns(2)
        with meta_col1:
            st.caption(f"👤 **Developer:** {selected_post['user']['name']}")
        with meta_col2:
            st.caption(f"🗓️ **Posted:** {selected_post['readable_publish_date']}")
            
        # Display Tags
        tags_str = " ".join([f"`#{t}`" for t in selected_post.get("tag_list", [])])
        st.markdown(f"🏷️ **Tags:** {tags_str}")
        
        st.write(selected_post.get("description", "No description available."))
        
        # Action button to full code/article
        st.link_button("🌐 Open Source Post on Dev.to", selected_post["url"])
