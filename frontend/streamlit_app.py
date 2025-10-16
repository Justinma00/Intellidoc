import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None

def make_api_request(endpoint, method="GET", data=None, files=None):
    """Make authenticated API request."""
    headers = {}
    if st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            if files:
                response = requests.post(url, headers=headers, files=files, data=data)
            else:
                headers["Content-Type"] = "application/json"
                response = requests.post(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        if response.status_code == 401:
            st.session_state.token = None
            st.session_state.user = None
            st.error("Session expired. Please login again.")
            return None
        
        return response.json() if response.content else {}
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def login_page():
    """Login/Register page"""
    st.title("🔐 IntelliDoc Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to your account")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                response = requests.post(
                    f"{API_BASE_URL}/auth/login",
                    data={"username": email, "password": password}
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]
                    
                    # Get user info
                    user_response = make_api_request("/auth/me")
                    if user_response:
                        st.session_state.user = user_response
                        st.success("Login successful!")
                        st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        st.subheader("Create new account")
        with st.form("register_form"):
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_password_confirm = st.text_input("Confirm Password", type="password")
            reg_submitted = st.form_submit_button("Register")
            
            if reg_submitted:
                if reg_password != reg_password_confirm:
                    st.error("Passwords don't match")
                else:
                    response = requests.post(
                        f"{API_BASE_URL}/auth/register",
                        json={"email": reg_email, "password": reg_password}
                    )
                    
                    if response.status_code == 200:
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Registration failed")

def dashboard_page():
    """Main dashboard page"""
    st.title("📊 IntelliDoc Dashboard")
    
    # Get dashboard stats
    stats = make_api_request("/analytics/dashboard")
    
    if stats:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documents", stats["total_documents"])
        
        with col2:
            st.metric("Processed", stats["processed_documents"])
        
        with col3:
            st.metric("Processing Rate", f"{stats['processing_rate']:.1f}%")
        
        with col4:
            st.metric("Vector Store", stats["vector_store_stats"]["total_documents"])
        
        # Category distribution chart
        if stats["category_distribution"]:
            st.subheader("📁 Document Categories")
            
            df_categories = pd.DataFrame(stats["category_distribution"]) if stats["category_distribution"] else pd.DataFrame(columns=["category","count"])
            fig = px.pie(df_categories, values='count', names='category', 
                        title="Document Distribution by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent documents
        if stats["recent_documents"]:
            st.subheader("📄 Recent Documents")
            
            for doc in stats["recent_documents"]:
                with st.expander(f"📄 {doc['filename']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Category:** {doc['category'] or 'Uncategorized'}")
                    with col2:
                        st.write(f"**Created:** {str(doc['created_at'])[:10]}")

def documents_page():
    """Documents management page"""
    st.title("📄 Document Management")
    
    tab1, tab2, tab3 = st.tabs(["Upload", "My Documents", "Search"])
    
    with tab1:
        st.subheader("📤 Upload New Document")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png'],
            help="Supported formats: PDF, DOCX, TXT, JPG, PNG"
        )
        
        category = st.selectbox(
            "Category (optional)",
            ["", "contract", "invoice", "legal", "financial", "technical", "medical", "academic", "other"]
        )
        
        if uploaded_file and st.button("Upload Document"):
            with st.spinner("Uploading and processing document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"category": category} if category else {}
                
                result = make_api_request("/documents/upload", method="POST", files=files, data=data)
                
                if result:
                    st.success(f"Document '{result['original_filename']}' uploaded successfully!")
                    st.json(result)
    
    with tab2:
        st.subheader("📋 My Documents")
        
        # Get documents
        documents = make_api_request("/documents/")
        
        if documents:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                category_filter = st.selectbox(
                    "Filter by category",
                    ["All"] + list(set([doc.get("category", "other") for doc in documents if doc.get("category")]))
                )
            
            # Display documents
            filtered_docs = documents
            if category_filter != "All":
                filtered_docs = [doc for doc in documents if doc.get("category") == category_filter]
            
            for doc in filtered_docs:
                with st.expander(f"📄 {doc['original_filename']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Category:** {doc.get('category', 'Uncategorized')}")
                        st.write(f"**Size:** {doc['file_size']} bytes")
                    
                    with col2:
                        st.write(f"**Created:** {doc['created_at'][:10]}")
                        if doc.get('confidence_score'):
                            st.write(f"**Confidence:** {doc['confidence_score']:.2f}")
                    
                    with col3:
                        if st.button(f"Delete", key=f"delete_{doc['id']}"):
                            if make_api_request(f"/documents/{doc['id']}", method="DELETE"):
                                st.success("Document deleted!")
                                st.rerun()
                    
                    # Show summary if available
                    if doc.get('summary'):
                        st.write("**Summary:**")
                        st.write(doc['summary'])

                    # Show content preview
                    if doc.get('content'):
                        st.write("**Content Preview:**")
                        st.text_area("Content",
                                     doc['content'][:1000] + "..." if len(doc['content']) > 1000 else doc['content'],
                                     height=200, key=f"content_{doc['id']}")
                    
                    # Query document
                    query = st.text_input(f"Ask a question about this document", key=f"query_{doc['id']}")
                    if query and st.button(f"Ask", key=f"ask_{doc['id']}"):
                        with st.spinner("Generating answer..."):
                            answer = make_api_request(
                                f"/documents/{doc['id']}/query",
                                method="POST",
                                data={"query": query}
                            )
                            if answer:
                                st.write("**Answer:**")
                                st.write(answer['answer'])
                                st.write(f"**Confidence:** {answer['confidence']:.2f}")
    
    with tab3:
        st.subheader("🔍 Search Documents")
        
        search_query = st.text_input("Search across all your documents")
        
        if search_query and st.button("Search"):
            with st.spinner("Searching..."):
                results = make_api_request(
                    "/documents/search",
                    method="POST",
                    data={"query": search_query}
                )
                
                if results and results.get('results'):
                    st.write(f"Found {results['total_found']} results:")
                    
                    for result in results['results']:
                        with st.expander(f"📄 {result['metadata']['filename']} (Score: {1-result['distance']:.2f})"):
                            st.write(result['document'][:500] + "..." if len(result['document']) > 500 else result['document'])
                            st.write(f"**Category:** {result['metadata'].get('category', 'Unknown')}")
                else:
                    st.write("No results found.")

def ai_tools_page():
    """AI Tools page"""
    st.title("🤖 AI Tools")
    
    tab1, tab2, tab3 = st.tabs(["Text Analysis", "Translation", "Q&A"])
    
    with tab1:
        st.subheader("📝 Text Analysis")
        
        text_input = st.text_area("Enter text to analyze", height=200)
        
        if text_input and st.button("Analyze Text"):
            with st.spinner("Analyzing..."):
                # Simulate text analysis (you would call actual AI service)
                st.write("**Analysis Results:**")
                
                # Word count
                words = len(text_input.split())
                st.metric("Word Count", words)
                
                # Simple sentiment analysis placeholder
                if "good" in text_input.lower() or "great" in text_input.lower():
                    sentiment = "Positive"
                elif "bad" in text_input.lower() or "terrible" in text_input.lower():
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"
                
                st.write(f"**Sentiment:** {sentiment}")
    
    with tab2:
        st.subheader("🌐 Translation")
        
        source_text = st.text_area("Text to translate", height=100)
        target_lang = st.selectbox("Target Language", ["Spanish", "French", "German", "Italian"])
        
        if source_text and st.button("Translate"):
            st.write("**Translation:**")
            st.write(f"[Translation to {target_lang} would appear here]")
    
    with tab3:
        st.subheader("❓ Document Q&A")
        
        st.write("Upload a document and ask questions about it using the Documents page!")

def main():
    """Main application"""
    st.set_page_config(
        page_title="IntelliDoc",
        page_icon="📄",
        layout="wide"
    )
    
    # Sidebar
    if st.session_state.token:
        st.sidebar.title("📄 IntelliDoc")
        st.sidebar.write(f"Welcome, {st.session_state.user.get('email', 'User')}")
        
        # Navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Dashboard", "Documents", "AI Tools"]
        )
        
        if st.sidebar.button("Logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
        
        # Main content
        if page == "Dashboard":
            dashboard_page()
        elif page == "Documents":
            documents_page()
        elif page == "AI Tools":
            ai_tools_page()
    
    else:
        login_page()

if __name__ == "__main__":
    main()