from rest_framework.throttling import UserRateThrottle

class QuestionThrottle(UserRateThrottle):
    scope = 'question'

    # def allow_request(self, request, view):

    #     if request.method == 'GET':
    #         return True

    #     if 'question-' + request.method.lower() in self.THROTTLE_RATES:
    #         self.scope = 'question-' + request.method.lower()
    #         self.rate = self.get_rate()
    #         self.num_requests, self.duration = self.parse_rate(self.rate)
            
        
    #     return super().allow_request(request, view)

class QuestionGetThrottling(UserRateThrottle):
    scope = 'question-get'

class QuestionPostThrottling(UserRateThrottle):
    scope = 'question-post'