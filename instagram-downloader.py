import instaloader
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Instagram Downloader", layout="wide")

@st.cache_resource
def init_instaloader():
    return instaloader.Instaloader()

L = init_instaloader()
L.login('USERNAME','PASSWORD')


st.title("Instagram Downloader")
st.markdown('''
            This is a Instagram Downloader app. Copy and Paste the insta url of the post you want to download. 
            
            ''')

post_url=st.text_input("Paste the insta url")

if post_url:
    short_url=post_url.split('p/')[1].strip('/ ').split('/?')[0]
    st.write("Short Code : "+short_url)
    post = instaloader.Post.from_shortcode(L.context, short_url)


    print("-----------------------------------------------------------")

    print(post_url)


    data={'likes': post.likes,
    'comments':post.comments,
    'captions': post.caption,
    'hashtags': post.caption_hashtags,
    'location':post.location,

    'mentions':post.caption_mentions,
    'tags':post.tagged_users,
    'media count':post.mediacount,
    'date posted':post.date,
    'profile name':post.profile,
    'is video':post.is_video
    }

    df = pd.DataFrame(list(data.items()), columns=['Keys','Values'])
    print(df)

    #index = ['likes', 'comments', 'captions', 'hashtags', 'location','mentions', 'tags', 'media count','date posted','profile name' ]

    #st.dataframe(df, use_container_width=True)
    st.table(df)

  

    col1,col2=st.columns(2)

    with col1:
         st.download_button(label="Download data as CSV",
        data=df.to_csv().encode('utf-8'),
        file_name=f'{short_url}'+'.csv',
        mime='text/csv')

    with col2:
       
        download_post_button=st.button("Download Post")


    if download_post_button:
       
       if post.is_video == False:
        urls=[node.display_url for node in post.get_sidecar_nodes()]
        for i,url in enumerate(urls):
            response = requests.get(url)
            try:
                open(f"{short_url}{i}"+".jpg", "wb").write(response.content)
            except:
                print("could not download file")
        st.success("Post downloaded successfully") 
       else:
        st.error("This option does not support video downloads")    


    import streamlit.components.v1 as components
    components.iframe(f"https://www.instagram.com/p/{short_url}/embed/",width=600, height=1000, scrolling=False)


  
