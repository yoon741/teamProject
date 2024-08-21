# /templates/include 디렉토리
+ 반복적으로 페이지에 나타나는 요소들 모듈화 한 곳
+ base는 레이아웃
  + <html lang="ko">

  + <head>  
    + <title>{% block title %}{% endblock %}</title>
    + {% block style %}{% endblock %}
  + </head>
    
  + <body>
    + {% include 'include/header.html' %}
    + <main>
      + {% block main %}{% endblock %}
    + </main>
    + {% include 'include/footer.html' %}
    + {% block script %}{% endblock %}
  + </body>
    
  + </html>

+ 헤더 위 푸터 아래