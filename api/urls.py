from django.urls import path
from api.views import scholarAuthentication,scholarCommunicate,notificationApi,reviewsApi

urlpatterns = [

    path('requestScholarAuth', scholarAuthentication.requestScholarAuthenticate),
    path('validScholarAuth', scholarAuthentication.validateScholarAuthentication),
    path('follow',scholarCommunicate.followScholar),
    path('getFollowList',scholarCommunicate.getFollowList),
    path('getAuthor',scholarCommunicate.getAuthorListFromEs),

    #private message
    path('requestPM',scholarCommunicate.requestPrivateMessage),
    path('getChatBoxList',scholarCommunicate.getRequest),
    path('replyRequest',scholarCommunicate.replyRequest),
    path('getChatBoxMessage',scholarCommunicate.getChatBoxMessage),
    path('sendMessage',scholarCommunicate.sendMessage),

    #notification
    path('getNotification',notificationApi.getNotification),
    path('checkNotification',notificationApi.checkNotification),
    
    #review
    path('reviewArticle',reviewsApi.createArticleReview),
    path('replyReview',reviewsApi.replyReview),
    path('getReviewList',reviewsApi.getReview),

]
