import streamlit as st
from db_utils import save_case

def render():
    # Check if form has been submitted and show confirmation
    if "form_submitted" in st.session_state and st.session_state.form_submitted:
        # Confirmation Page
        st.title("Report Successfully Submitted!")
        
        # Success message
        st.success("Your report has been filed and is now under review. Our team will investigate the matter and take appropriate action.")
        
        # Display submitted information in a nice format
        st.markdown("---")
        st.markdown("### Report Summary")
        
        data = st.session_state.submitted_data
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Platform Information:**")
            st.info(f"Platform: {data['platform']}")
            st.info(f"Source URL: {data['url']}")
            
            st.markdown("**Flagging Details:**")
            st.warning(f"Reason: {data['reason']}")
            
        with col2:
            st.markdown("**Evidence Type:**")
            st.info(f"Type: {data['evidence_type']}")
            
            # Show evidence details based on type
            if data['evidence_type'] == "Post Text" and data['post_text']:
                st.markdown("**Post Content:**")
                st.text_area("Reported Text:", value=data['post_text'], height=100, disabled=True)
                
            elif data['evidence_type'] == "Image Match" and data['image_match_url']:
                st.markdown("**Image Match:**")
                st.info(f"Image URL: {data['image_match_url']}")
                
            elif data['evidence_type'] == "Screenshot/Image" and data['image_uploaded']:
                st.markdown("**Evidence:**")
                st.success("Screenshot/Image uploaded successfully")
        
        # Additional information if provided
        if data.get('additional_info'):
            st.markdown("**Additional Information:**")
            st.text_area("Additional Details:", value=data['additional_info'], height=80, disabled=True)
        
        st.markdown("---")
        
        # Timestamp
        if 'timestamp' in data:
            st.caption(f"Submitted on: {data['timestamp']}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Another Report", type="primary"):
                # Clear session state and reset form
                st.session_state.form_submitted = False
                if "submitted_data" in st.session_state:
                    del st.session_state.submitted_data
                st.rerun()
        
        with col2:
            if st.button("Go to Home"):
                # Clear session state and navigate to home
                st.session_state.form_submitted = False
                if "submitted_data" in st.session_state:
                    del st.session_state.submitted_data
                st.session_state.current_page = "Home"
                st.rerun()
        
        # Information box
        st.info("**What happens next?**\n- Our team will review your report within 24-48 hours\n- If the report is valid, appropriate action will be taken\n- You may receive follow-up communication if additional information is needed")
        
        return  # Exit early to prevent form from showing

    # Regular form page
    st.title("Evidence & Contextualization")
    st.markdown("Report suspicious content, fake accounts, or misinformation to help keep our digital space safe.")
    
    st.markdown("---")

    with st.form(key="evidence_form"):
        st.markdown("### Report Details")
        
        # Platform and URL
        col1, col2 = st.columns(2)
        with col1:
            platform = st.text_input("Source Platform", placeholder="e.g., Facebook, Twitter, Instagram")
        with col2:
            url = st.text_input("Source URL", placeholder="https://...")
        
        # Evidence type selection
        st.markdown("### Evidence Type")
        evidence_option = st.radio(
            "What type of evidence are you submitting?",
            ["Screenshot/Image", "Post Text", "Image Match"],
            help="Choose the type of evidence that best describes your report"
        )
        
        # Initialize variables
        screenshot_bytes = None
        post_text = ""
        image_match_url = ""
        
        # Evidence-specific inputs
        st.markdown("---")
        if evidence_option == "Screenshot/Image":
            st.markdown("### Upload Evidence")
            screenshot = st.file_uploader(
                "Upload Screenshot or Image", 
                type=["png", "jpg", "jpeg"],
                help="Upload a screenshot or image that shows the suspicious content"
            )
            if screenshot is not None:
                screenshot_bytes = screenshot.read()
                st.success("File uploaded successfully!")
                # Show image preview
                st.image(screenshot_bytes, caption="Uploaded Evidence", width=300)
                
        elif evidence_option == "Post Text":
            st.markdown("### Post Content")
            post_text = st.text_area(
                "Paste the suspicious post text here",
                height=150,
                help="Copy and paste the exact text content that you want to report"
            )
            
        else:  # Image Match
            st.markdown("### Image Match")
            image_match_url = st.text_input(
                "URL of the matched/similar image",
                help="Provide the URL of an image that matches or is similar to the suspicious content"
            )
        
        st.markdown("---")
        
        # Reason for flagging
        st.markdown("### Flagging Information")
        reason = st.selectbox(
            "Primary reason for flagging this content:",
            [
                "Fake Account",
                "Image Misuse", 
                "Data Leak",
                "Misinformation/Disinformation",
                "Spam",
                "Other"
            ]
        )
        
        # Additional information
        additional_info = st.text_area(
            "📝 Additional Information (Optional)",
            help="Provide any additional context or details that might help with the investigation",
            height=100
        )
        
        st.markdown("---")
        
        # Terms and submit
       # Submit button
        submitted = st.form_submit_button(
            "Submit Report", 
            type="primary",
            help="Click to submit your report for review"
        )

        
        # Form validation and submission
        if submitted:
            # Basic validation
            if not platform or not url:
                st.error("❌ Please fill in both Platform and URL fields")
                return
            
            if evidence_option == "Post Text" and not post_text:
                st.error("❌ Please provide the post text for this evidence type")
                return
            
            if evidence_option == "Image Match" and not image_match_url:
                st.error("❌ Please provide the image URL for this evidence type")
                return
            
            if evidence_option == "Screenshot/Image" and not screenshot_bytes:
                st.error("❌ Please upload a screenshot or image file")
                return
            
            # Save to database
            try:
                save_case(
                    platform,
                    url,
                    evidence_option,
                    screenshot_bytes,
                    post_text,
                    image_match_url,
                    reason,
                    additional_info,
                )
                
                # Store submission data for confirmation page
                from datetime import datetime
                st.session_state.form_submitted = True
                st.session_state.submitted_data = {
                    "platform": platform,
                    "url": url,
                    "evidence_type": evidence_option,
                    "post_text": post_text,
                    "image_match_url": image_match_url,
                    "reason": reason,
                    "additional_info": additional_info,
                    "image_uploaded": bool(screenshot_bytes),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error submitting report: {str(e)}")
                st.error("Please try again or contact support if the problem persists")