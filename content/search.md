
#### title: a search tool
#### tags: search tool 

<h2>Search with Woosh~</h2>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js">
</script>

<div>
    <div>
        <label for="type">Type:</label>
        <input type="text" id="type" name="type" size="50" value="eg. tags, content etc"/>
    </div>
    <div>
        <label for="query">Query:</label>
        <input type="text" id="query" name="query" size="50"/>
    </div>
    <div>
        <label for="page">Page:</label>
        <input type="number" id="page" name="page" size="10"/>
    </div>
    <div>
        <p id="go" style="border: 1px;">Go</p>
    </div>
    <hr/>
    <div id="results">
    </div>
</div>

<script>  
    $(document).ready(function() {  
        $("#go").on("click", function() {
            var type = $("#type").val();
            var query = $("#query").val();
            var page = $("#page").val();
            if (query.length > 0) {
                $.ajax({
                    url: "/search", 
                    type: "GET",
                    data: {
                        type: type, 
                        query: query,
                        page: page
                    },
                    success: function(data) {
                        $("#results").html(data);
                    }
                });
            } else {
                $("#results").empty(); 
            }
        });
    });
</script>