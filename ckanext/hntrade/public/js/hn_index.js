$(function() {

	$(".dataset_des").each(function(i) {
		var divH = $(this).height();
		var $p = $("p", $(this)).eq(0);
		while($p.outerHeight() > divH) {
			$p.text($p.text().replace(/(\s)*([a-zA-Z0-9]+|\W)(\.\.\.)?$/, "..."));
		};
	});

	//���� main �е� prod logo
	function setprod(){
		for(var i = 1; i <= 12; i++) {
			var ui = "/img/govDatasetsLogo/gl_" + i + ".png";
			$("#prod" + i + " .hn_image").css({
				"background": "url(" + ui + ")",
				"background-size": "70px 70px"
			});
		}
		for(var i = 1; i <= 4; i++) {
			var pi = "/img/govDatasetsLogo/pp" + i + ".png";
			$("#pp"+i).css({
				"background": "url(" + pi + ")",
				"background-size": "30px 30px"
			});
			$("#new"+i).css({
				"background": "url(" + pi + ")",
				"background-size": "30px 30px"
			});
		}
	}
	setprod();
	//����hover����
	function prodHover(){
		$(".prod").hover(function(){
			var i = $(this).attr("id");
			i = i.substring(4,i.length);
			var uih = "img/govDatasetsLogo/gl_" + i + "_hover.png";
			$(this).children(".hn_image").css({
				"background": "url(" + uih + ")",
				"background-size": "70px 70px"
			});
		},function(){
			var j = $(this).attr("id");
			j = j.substring(4,j.length);
			var ui = "img/govDatasetsLogo/gl_" + j + ".png";
			$(this).children(".hn_image").css({
				"background": "url(" + ui + ")",
				"background-size": "70px 70px"
			});
		});
	}
	prodHover();
    	var mySwiper = new Swiper('.swiper-container', {
		// �����Ҫ��ҳ��
		pagination: '.swiper-pagination',
		paginationClickable: true,
		preventClicksPropagation: true, //�϶�ʱ��ֹ����¼�ð��
		loop: true,
		autoplay: 3600,
		grabCursor: true,

		//������
		//scrollbar:'.swiper-scrollbar',

		// �����Ҫǰ�����˰�ť
		nextButton: '.swiper-button-next',
		prevButton: '.swiper-button-prev',

		//Ч��
		effect: "slide",
	})
});