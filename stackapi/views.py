from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication,permissions
from .serializers import QuestionSerializer,AnswerSerializer
from stack.models import Questions,Answers
from rest_framework.decorators import action
from stackapi.custompermissions import OwnerOrReadOnly
from rest_framework import mixins,generics
from rest_framework import serializers
# Create your views here.

class QuestionsView(viewsets.ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    http_method_names=["get","post","put"]
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

    @action(methods=["POST"],detail=True)
    def add_answer(self,request,*args, **kwargs):
        question=self.get_object()
        user=request.user
        serializer=AnswerSerializer(data=request.data,context={"user":user,"question":question})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class QuestionDeleteView(mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Questions.objects.all()
    serializer_class=QuestionSerializer
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[OwnerOrReadOnly]
    def delete(self,request,*args, **kwargs):
        return self.destroy(request,*args,**kwargs)

class AnswersView(viewsets.ViewSet):
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated,OwnerOrReadOnly]
    # localhost:8000/answers/1/up_vote/
    @action(methods=["POST"],detail=True)
    def add_up_vote(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        answer=Answers.objects.get(id=id)
        user=request.user
        answer.up_vote.add(user)
        answer.save()
        return Response(data="upvoted")

    # localhost:8000/answers/8/
    # delete
    def destroy(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        object=Answers.objects.get(id=id)
        if object.user==request.user:
            Answers.objects.filter(id=id).delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("you do not have permissions")