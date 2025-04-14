mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headles = true\n\
\n\
" > ~/.streamlit/config.toml