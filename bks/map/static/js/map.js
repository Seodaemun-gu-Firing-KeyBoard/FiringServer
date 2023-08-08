const naverMapApiKey = "2lhimp3vcd";

function map() {
  //지도를 띄울 div의 ID요소
  const mapElement = document.getElementById("map");

  //초기 지도 상태
  const mapOptions = {
    //초기 지도 좌표 : 명지대 인문캠퍼스
    center: new naver.maps.LatLng(37.580541, 126.922365),
    // 초기 확대량
    zoom: 17,
  };

  //네이버 지도 객체 생성
  const map = new naver.maps.Map(mapElement, mapOptions);
}

document.addEventListener("DOMContentLoaded", function () {
  map();
});
