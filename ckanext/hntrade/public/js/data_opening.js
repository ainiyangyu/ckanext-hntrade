 $().ready(function(){
            $('.cc-selector-li1 .cc-content-limit-active').each(function(index,element){
                if(index>13){
                    $(this).hide();
                }
            })
        })
        //左侧导航栏1
        $('.cc-left-title1').on('click',function(){

            var isShow= $(this).siblings('.cc-data-catagory-container1').css('display');
            if(isShow=='none'){
                $('.cc-data-catagory-container1').hide();
                $(this).siblings('.cc-data-catagory-container1').show();
                $('.do-top-bottom1').attr('src','img/dataOpening/toBottom.png');
                $(this).find('.do-top-bottom1').attr('src','img/dataOpening/toTop.png');
                $(this).parent().siblings().find('.do-top-bottom1').attr('src','img/dataOpening/toBottom.png');
            }else if(isShow=='block'){
                $(this).siblings('.cc-data-catagory-container1').hide();
                $(this).parent().siblings().find('.cc-data-catagory-container1').show();
                $(this).find('.do-top-bottom1').attr('src','img/dataOpening/toBottom.png');
                $(this).parent().siblings().find('.do-top-bottom1').attr('src','img/dataOpening/toTop.png');
            }
            
        })
        //左侧导航栏2
        $('.cc-left-title2').on('click',function(){

            var isShow= $(this).siblings('.cc-data-catagory-container2').css('display');
            if(isShow=='none'){
                $('.cc-data-catagory-container2').hide();
                $(this).siblings('.cc-data-catagory-container2').show();
                $('.do-top-bottom2').attr('src','img/dataOpening/toBottom.png');
                $(this).find('.do-top-bottom2').attr('src','img/dataOpening/toTop.png');
                $(this).parent().siblings().find('.do-top-bottom2').attr('src','img/dataOpening/toBottom.png');
            }else if(isShow=='block'){
                $(this).siblings('.cc-data-catagory-container2').hide();
                $(this).parent().siblings().find('.cc-data-catagory-container2').show();
                $(this).find('.do-top-bottom2').attr('src','img/dataOpening/toBottom.png');
                $(this).parent().siblings().find('.do-top-bottom2').attr('src','img/dataOpening/toTop.png');
            }

        })
        //点击 更多
        $('.do-list-more').on('click',function(){
            if($(this).text()=='收起'){
                $(this).text('更多');
                 $('.cc-selector-li1 .cc-content-limit-active').each(function(index,element){
                    if(index>13){
                        $(this).hide();
                    }
                })
            }else if($(this).text()=='更多'){
                 $(this).text('收起');
                 $('.cc-selector-li1 .cc-content-limit-active').show()
            }
            
        })

        //点击条件选中
        $('.cc-content-limit-active').on('click',function(){
            
            var index= $(this).parents('tr').index();
                if(!$(this).parents('tr').hasClass('isClicked')){
                    $(this).addClass('isselected');
                    $(this).addClass('cc-content-limit-active');
                    var name= $(this).parent().siblings('.cc-selector-catagory').text();
                    var value= $(this).text();
                    var html="<span class='cc-content-condition-all'><img data-index="+index+" onclick='removeCondition(this)' class='cc-close-s' src='img/commodityCatagory/cc-close.png'/>"+name+"<span class='cc-selected-item'>"+value+"</span>"+"</span>";
                    $('.cc-content-condition-container').append(html);
                    $(this).parents('tr').addClass('isClicked');
                }
            
        })
        //close
        function removeCondition(obj){
            var index= $(obj).attr("data-index");
            $('.cc-selector-adding-table').find('tr').eq(index).removeClass('isClicked');
            $(obj).parent().remove();
            $(obj).siblings('.cc-selected-item').text();
            $('.cc-content-limit-active').removeClass('isselected');
        }   
        //selector
        $('.cc-imitate-result').on('click',function (){
            $(this).siblings().show();
        }) 
        //伪selector 鼠标离开时自动隐藏
        $('.cc-imitate-selector-li').on('click',function(){
            var text= $(this).text();
            $(this).parents('.cc-imitate-selector').find('.cc-imitate-result').text(text);
            $(this).parents('.cc-imitate-selector-container').hide();
        })
        //伪selector 鼠标离开时自动隐藏
         $('.cc-imitate-selector-container').mouseleave(function(){
           $(this).hide();
       })
