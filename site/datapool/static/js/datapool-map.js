function DatapoolMap(){
    this.map = null;
    this.basemap = "zimmerman2014.hmpkg505";
    this.tl = null;
    this.filters = null;
    this.project_id = 0;
    this.loaded = 0;
    this.search_boxes_loaded = false;

    if (typeof standard_basemap !== 'undefined') {
        this.basemap = standard_basemap;
    }

    this.set_map = function(div_id, zoomposition, no_dragging){

        var mapoptions = {
            attributionControl: false,
            scrollWheelZoom: false,
            zoom: 11,
            minZoom: 9,
            maxZoom:15,
            continuousWorld: 'false',
            zoomControl: 'true'
        }

        if(no_dragging){
            mapoptions.dragging = false;
        }

        // if(zoomposition || zoomposition == null){
        //     mapoptions.zoomControl = false;
        // }

        jQuery("#"+div_id).css("min-height", "450px");
        jQuery("#"+div_id).css("min-width", "450px");
        this.map = L.map(div_id, mapoptions).setView([-1.292066, 36.821946], 11);

        if (zoomposition){
            new L.Control.Zoom({ position: zoomposition }).addTo(this.map);
        }

        this.tl = L.tileLayer('https://{s}.tiles.mapbox.com/v3/'+this.basemap+'/{z}/{x}/{y}.png', {
            maxZoom: 15
        }).addTo(this.map);

        this.heat = [];

        this.heat[0] = L.heatLayer([], {
            minOpacity: .5,
            radius: 18,
            blur: 25,
            gradient: {0.5: 'rgba(0,255,255,0.1)', 0.7: 'rgba(0,153,255,0.1)', 1: 'rgba(51,102,255,0.1)'}
        }).addTo(this.map);

        this.heat[1] = L.heatLayer([], {
            minOpacity: .5,
            radius: 18,
            blur: 25,
            gradient: {0.5: 'rgba(204,204,0,0.1)', 0.7: 'rgba(255,102,0,0.1)', 1: 'rgba(204,0,0,0.1)'}
        }).addTo(this.map);
        this.refresh(false,0);
    };

    this.resetData = function(){
        

        this.heat[0].setLatLngs([]);
        this.heat[1].setLatLngs([]);
    }

    this.refresh = function(data, heatmapId){
        if(data){
            this.resetData();
            this.reDraw(data, heatmapId);
        } else{
            this.resetData();
            this.loaded = 0;
            this.getData(data, 0);
        }
    };

    this.createUrl = function(heatmapId){

        var url = '/get_project_chart_data/'+this.project_id+'/heat_map/';
        //console.log('get url = '+url);
        return url;
    }


    this.getData = function(url, heatmapId){
        var url = this.createUrl(heatmapId);
        var that = this;
        jQuery.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            data:$("#heatmap-search-"+this.project_id).serialize(),
            success: function(data){
                
                data = that.formatData(data);
                 if(that.search_boxes_loaded == false){
                    that.addSearchBoxes()
                }

                that.refresh(data, heatmapId);
            }
        });
    };

    this.formatData = function(data){
        var formattedData = {};
       
        for(var j = 0;j < data.length;j++){

            

            data_set = data[j]['data'];
            this.search_boxes = data[j]['search_boxes'];
            types = data[j]['property_type_set'];
            //console.log(data[j]);
            lat_field = '';
            long_field = '';
            for(prop in types){
                //console.log(types);
                if (types[prop]['type'] == 'LAT'){
                    lat_field = prop;

                }
                if (types[prop]['type'] == 'LONG'){
                    long_field = prop;

                }

            }
            //console.log(lat_field+' '+long_field);
            formattedData[j] = {}
            formattedData[j]['data_set'] = []
            for(var i = 0; i < data_set.length;i++){
                
                    formattedData[j]['data_set'][i] = {}

                    formattedData[j]['data_set'][i]['latitude'] = data_set[i][lat_field];
                    formattedData[j]['data_set'][i]['longitude'] = data_set[i][long_field];
                
            }
        }
        
        //console.log(return_arr);
        return formattedData;


    }
    this.reDraw = function(data, heatmapId){
        console.log(data.length);
        for ( i in data){
            data_set = data[i]['data_set'];
           // console.log('formattedData = ');
            //console.log(data_set);
            for (j in data_set){
                if(data_set[j]['latitude'] == undefined || data_set[j]['longitude'] == undefined){
                    continue;
                }
                //console.log(data_set[j]['latitude']);
                this.heat[i].addLatLng([data_set[j]['latitude'], data_set[j]['longitude']]);
            }

        }

     
    }
    this.addSearchBoxes = function(){
        for(box_id in this.search_boxes){
            $('.searchboxes-heatmap-'+this.project_id).append("<div>"+this.search_boxes[box_id]['name']+"<input type='text' name='"+box_id+"' id='"+box_id+"'/></div>");
        }
        this.search_boxes_loaded = true;
    }

}