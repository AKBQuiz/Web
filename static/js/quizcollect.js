var appcollect = angular.module('collectapp', []);

appcollect.controller('CollectCtrl', ['$scope','$http', function ($scope,$http) {

  $scope.quiz = {
    author: "",
    group: [false,false,false,false,false,false,false,false],
    question: "",
    difficulty: 0,
    answer: "",
    wrong: [" "," "," "]
  }

  $scope.stopalert = function(){
    if ($scope.alertclosable){ $scope.alerting = false; }
  }

  $scope.doalert = function(text,closable){
    $scope.alertclosable = closable;
    $scope.alerttext = text;
    $scope.alerting = true;
  }

  $scope.query = function(){
    if ($scope.quizinfo.author.$valid) 
      window.open('./query/?author=' + encodeURI($scope.quiz.author),'','');
  }

  $scope.rank = function(){
    this.quiz.difficulty++;
    if ( this.quiz.difficulty > 5 ) { this.quiz.difficulty=0; }
  }

  $scope.reset = function(){
    this.quiz.group = [false,false,false,false,false,false,false,false];
    this.quiz.question = " ";
    this.quiz.difficulty = 0;
    this.quiz.answer = " ";
    this.quiz.wrong = [" "," "," "];
  }

  $scope.submit = function(){
    if (!$scope.quizinfo.$valid) {
      $scope.doalert("请检查项目",true);
      return;
    };
    if ($scope.isSending) return;
    $scope.doalert("正在提交...",false);
    $scope.isSending = true;
    $http.post("../api/collect/",this.quiz).success(function(data) {
      if (data == "success") {
        $scope.reset();
        $scope.alerttext = "提交成功！ 请等待管理员通过审核（可能会有很长时间的延迟 >.< ）";
        $scope.alertclosable = true;
      }else{
        $scope.alerttext = "提交失败！ Info: " + data;
        $scope.alertclosable = true;
      };
      $scope.isSending = false;
    }).error(function(data, status, headers, config){
      $scope.alerttext = "网络连接失败！";
      $scope.alertclosable = true;
      $scope.isSending = false;
    });
  }
}]);
