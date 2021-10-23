document.addEventListener("DOMContentLoaded", function(event) {
    var player = document.getElementById("bg_video");
    if(player) 
        player.playbackRate = 0.5;

    var menu=document.getElementById('menu');   
        menu.addEventListener("click",function()
        {
           menu.classList.toggle('menu-active');
        });
        
        var switchers_id = ['switcher_1', 'switcher_2', 'switcher_3'];
        var switchers = [];

        switchers_id.forEach(function(_id) {

            var switcher = document.getElementById(_id);

            if(switcher === null)
                return;

            switcher.addEventListener('click', _switch);
            switchers.push(switcher);

        });

        function _switch()
        {
            switchers.forEach(function(_iter) {

                let id = _iter.getAttribute('data-id');
                var container = document.getElementById(id);

                if(_iter.checked)
                    container.style.display = 'block';
                else
                    container.style.display = 'none';

            });
        }

        _switch();

    });
