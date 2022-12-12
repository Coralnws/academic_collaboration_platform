from django.urls import path
from api.views import scholarAuthentication,scholarCommunicate,notificationApi,reviewsApi,questionApi

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
    path('delNotification',notificationApi.deleteNotification),
    
    #review
    #path('reviewArticle',reviewsApi.createArticleReview),
    path('createReview',reviewsApi.createReview),
    path('getReviewList',reviewsApi.getReview),
    path('reportReview',reviewsApi.reportReview),
    path('manageReviewReport',reviewsApi.manageReviewReport),
    path('deleteReview',reviewsApi.deleteReview),

    #question
    path('createQuestion',questionApi.createQuestionReply),
    path('getQuestion',questionApi.getQuestionReply),



]
