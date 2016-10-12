// modules/About.js
import React from 'react';
// import { Link } from 'react-router';
import yaml from 'js-yaml';

export default function Project({ project : { owner, server, stack, stack : { docker_compose_file }, uuid }, deleteProject }) {
    // console.log('project props: ', owner, server, stack, uuid, deleteProject );

    function handleClick() {
        deleteProject(uuid);
    }

    var yamlConfig = yaml.safeLoad(docker_compose_file);

    var services = [];

    for (var key in yamlConfig.services) {
        if (yamlConfig.services.hasOwnProperty(key)) {
            if (yamlConfig.services[key].ports) {
                services.push(key);
            }
        }
    }

    return (
        <div className="m-y-2">
            <div>Project uuid: { uuid } </div>
            <div>Project owner: { owner } </div>
            <div>Stack: { stack.name } </div>
            <div>Server host: { server.host } </div>
            <div>Services: { services.join(', ') }</div>
            <button onClick={handleClick} className="btn btn--danger">Delete project</button>
            {/*<div>
                <Link to="/" activeOnlyWhenExact activeClassName="active">Back to projects</Link>
            </div>*/}
        </div>
    );
}
